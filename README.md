# zabbix-alertscript-maintenance
Alert script that allows Zabbix to enable/disable a maintenance window for a host.

## Why would I do this?
Zabbix maintenance modes are an extremely helpful concept, but they require an
admin level account.  Taking that a step further, most automation tools require
those same credentials in ways that can be troublesome for shared automation.

However, Zabbix has built in checks that can enable you to programatically
detemine a node's health and a trigger can say,
    "This host should be in maintenance!".

## Pre-requisites
* Currently the makefile and RPM are built around a Fedora/EPEL provided Zabbix 2.2+ install.  This is not required to run, but makes installing more of a chore.

## Installation
```make install```

or

```yum install zabbix-alertscript-maintenance```


## Configuration

### New Media Type
Zabbix uses Media types to expose custom alert functions.

* Administration -> Media types
* Create Media type
  * Name: Maintenance
  * Type: Script
  * Script name: maintenance-mode
  * Enabled: [checked]
  * Save

### Maintenance user and group
Media types are assigned to users, and the ability to manage maintenance mode requires admin access.

* We discourage using the Maintenance media for regular users.

#### Create a group
* Administration -> Users
* Select 'User group'
* Create user group
  * Group name: Maintenance
  * Frontend access: Disabled
  * Enabled: [checked]
  * Under Permissions:
    * Read-write -> Add: Select all
  * Save

#### Create a user
* Administration -> Users
* Select 'User'
* Create user
  * Alias: Maintenance
  * Groups: Add 'Maintenance'
  * Password: set a good one
  * Under Media:
    * Add
      * Type: Maintenance
      * Send to: api (this doesnt actually matter, but has to have something)
      * The rest can be default unless necessary for your environment
      * Add
  * Under Permissions:
    * User type: Zabbix Admin
  * Save

### Action
At this point the implementation can become very specific to the environment.  For the example (Plight)[https://github.com/rackerlabs/plight] will be used to provide the host state.  This project includes example templates for plight items and triggers.

* Configuration -> Actions
* Create action
  * Name: Manage maintenance mode
  * Default subject: ```{TRIGGER.STATUS}```
  * Default message: ```trigger_name:{TRIGGER.NAME}
trigger_id:{TRIGGER.ID}
host_name:{HOST.NAME}
event_id:{EVENT.ID}
maint_duration:{$PLIGHT_MAINT_PRD}
offline_duration:{$PLIGHT_OFFLINE_PRD}
```

  * Enabled: [checked]
  * Under Conditions
    * New trigger: Application = Plight mode
  * Under Operations
    * Operation Type: Send message
    * Send to Users: Maintenance
    * Send only to: Maintenance
    * Default message: [checked]
  * Add

### Triggers
If implementing a custom check instead of Plight there is only two requirements.  The trigger name for Maintenance mode should contain 'maintenance mode' and offline requires 'offline mode'

### Credentials
The configuration of the API user will be in ```/etc/zabbix/alertscripts/maintmode.conf```.

Here is a same of its contents.
```
[zabbix]
user=Maintenance
password=somereallygoodpassword
api=https://localhost/zabbix
```

## Testing the configuration and the installation.
To perform this test you will need the name of a host to put into maintenance mode. 'Zabbix server' exists on most systems by default.

To trigger maintenance mode:
```
/usr/lib/zabbix/alertscripts/maintenance-mode user PROBLEM "trigger_id:1
event_id:128
trigger_name:Node in maintenace mode
host_name:Zabbix server"
```

To remove that maintenance mode:
```
/usr/lib/zabbix/alertscripts/maintenance-mode user OK "trigger_id:1
event_id:128
trigger_name:Node in maintenace mode
host_name:Zabbix server"
```
