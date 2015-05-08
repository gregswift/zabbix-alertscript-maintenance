#!/usr/bin/env python

import requests
import configparser
import sys

CONFIG_FILE = '/etc/zabbix.d/maintmode.conf'

def get_config(config_file=CONFIG_FILE):
    return { 'user': 'Admin', 'password': 'AUJHIDnhr2MH', 'api': 'http://zabbix-dfw1.nytefyre.net/zabbix_api.php'}

def main():
    # The second argument is task, enable/disable
    task = _parse_zabbix_subject(sys.argv[2])
    # Third argument contains relevant host data
    details = _parse_zabbix_body(sys.argv[3])

    config = get_config()

    window_start = datetime.datetime.now()
    window_close = window_start + config['duration']

    name = ''