# id:{TRIGGER.ID}
# name:{TRIGGER.NAME}
# severity:{TRIGGER.SEVERITY}
# value:{TRIGGER.VALUE}
# hostname:{HOST.NAME}
# event_id:{EVENT.ID}

from datetime import datetime, timedelta
import time
from pyzabbix import ZabbixAPI, ZabbixAPIException

ZABBIX_ROOT = 'http://zabbix-dfw1.nytefyre.net'
URL = ZABBIX_ROOT + '/api_jsonrpc.php'

HEADERS = {
    'content-type': 'application/json',
}

def get_api():
	zapi = ZabbixAPI(ZABBIX_ROOT)
	zapi.login('Admin', 'AUJHIDnhr2MH')
	return zapi

def get_hostid(api, name):
	return api.host.get(name)[0][u'hostid']

def set_maint(api, name, duration=3600):
	hostid = get_hostid(api, name)
	now = time.mktime(datetime.now().timetuple())
	tomorrow = time.mktime( (datetime.now()+timedelta(seconds=duration)).timetuple() )
	method = 'maintenance.create'
	return api.maintenance.create(
		name=name,
		hostids=[ hostid ],
		active_since=now,
		active_till=tomorrow,
		timeperiods=[{
			"timeperiod_type": 0,
		}])

def clear_maint(api, name):
	hostid = get_hostid(api, name)
	maint_id = api.maintenance.get(name)[0][u'maintenanceid']
	return api.maintenance.delete(maint_id)
