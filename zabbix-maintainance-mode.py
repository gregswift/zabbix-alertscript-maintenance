#!/usr/bin/env python

import configparser
import sys
from datetime import datetime, timedelta
import time
from pyzabbix import ZabbixAPI, ZabbixAPIException

CONFIG_FILE = '/etc/zabbix.d/maintmode.conf'

def get_config(config_file=CONFIG_FILE):
    return {
        'user': 'Admin',
        'password': 'AUJHIDnhr2MH',
        'api': 'http://zabbix-dfw1.nytefyre.net' }

def get_api():
	zapi = ZabbixAPI(ZABBIX_ROOT)
	zapi.login('Admin', 'AUJHIDnhr2MH')
	return zapi

def get_hostid(api, name):
	return api.host.get(name)[0][u'hostid']

def get_maintid(api, name):
	return api.maintenance.get(name)[0][u'maintenanceid']

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
	maint_id = get_maintid(api, name)
	return api.maintenance.delete(maint_id)

def main():
    # The second argument is task, enable/disable
    enable_maint = _parse_zabbix_subject(sys.argv[2])
    # Third argument contains relevant host data
    details = _parse_zabbix_body(sys.argv[3])

    config = get_config()

    tmp_file = '/tmp/{0}-{1}'.format(details['trigger_id'],details['event_id'])
    outfile = open(tmp_file, 'a')
    outfile.write('trigger_status: {0}\n'.format(enable_maint))
    for k,v in details.iteritems():
        outfile.write('{0}: {1}\n'.format(k, v))
    api = get_api(config['api'],config['user'],config['password'])
    if enable_maint:
        outfile.write('{0}\n{1}\n'.format(details['host_name'], config['duration']))
        a = set_maint(api, details['host_name'], config['duration'])
        outfile.write('maintid: {0}\n'.format(a[u'maintenanceids'][0]))
    else:
    outfile.write('{0}\n'.format(details['host_name']))
        id = get_maintid(details['host_name'])
        outfile.write('maintid: {0}\n'.format(id))
        a = clear_maint(api, details['host_name'])
        outfile.write('cleared maintid: {0}\n'.format(a[u'maintenanceids'][0]))

if __name__ == '__main__':
    main()
