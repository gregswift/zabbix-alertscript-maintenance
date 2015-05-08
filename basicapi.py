# id:{TRIGGER.ID}
# name:{TRIGGER.NAME}
# severity:{TRIGGER.SEVERITY}
# value:{TRIGGER.VALUE}
# hostname:{HOST.NAME}
# event_id:{EVENT.ID}

import requests
from pprint import pprint
import json
from datetime import datetime, timedelta
import time
from pyzabbix import ZabbixAPI, ZabbixAPIException

ZABBIX_ROOT = 'http://zabbix-dfw1.nytefyre.net'
URL = ZABBIX_ROOT + '/api_jsonrpc.php'

HEADERS = {
    'content-type': 'application/json',
}

def query_api(method, params, url=URL, token=None):
        payload = {
            "jsonrpc" : "2.0",
            "method" : method,
            "params": params,
            "auth" : token,
            "id" : 0,
        }
        res  = requests.post(url, data=json.dumps(payload), headers=HEADERS)
        return res.json()

def auth():
        method = 'user.login'
        params = { 'user': 'Admin', 'password': 'AUJHIDnhr2MH' }
        res = query_api(method, params)
        return res['result']

def get_api():
	zapi = ZabbixAPI(ZABBIX_ROOT)
	zapi.login('Admin', 'AUJHIDnhr2MH')
	return zapi

def get_host(token, name):
	method = 'host.getobjects'
	params = {
		"name": name,
	}
	return query_api(method, params, token=token)

def get_maint(token):
        method = 'maintenance.get'
        params = {
        	"output": "extend",
	        "selectGroups": "extend",
        	"selectTimeperiods": "extend",
	    }
	return query_api(method, params, token=token)

def check_for_maint(token, name):
	method = 'maintenance.get'
	params = {
		"filter": {
			"host": [name]
		}
	}
	return query_api(method, params, token=token)

def set_maint(token, name, duration=3600):
	hostid = get_host(token, name)[u'result'][0][u'hostid']
	now = time.mktime(datetime.now().timetuple())
	tomorrow = time.mktime( (datetime.now()+timedelta(days=1)).timetuple() )
	method = 'maintenance.create'
	params = {
		"name": name,
		"hostids": [ hostid ],
		"active_since": now,
		"active_till": tomorrow,
		"timeperiods": [{
			"timeperiod_type": 0,
		}]
	}
	return query_api(method, params, token=token)
