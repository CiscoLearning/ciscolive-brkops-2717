# 1. Automate network changes
Automation of network changes can either be done by scripting directly down to networking devices by using for instance YANG models or by utilising a network controller such as Cisco DNA Center and levering its APIs. In this section we have created and shared two different script examples of how to automate network changes by either direct connection down to networking devices such as switches by using netconf or by scripting against Cisco DNA Center.

## Example 1: Network changes with NETCONF 
### YANG Models
YANG is a data modeling language which is used together with programmatic interfaces such as NETCONFin order to configure networking devices such as switches and routers. 

### Documentation
- [Introduction to Model Driven Programmability](https://developer.cisco.com/learning/modules/intro-device-level-interfaces/)
- [Netconf configuration and requirements](https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/prog/configuration/173/b_173_programmability_cg/configuring_yang_datamodel.html) 
- The [ncclient](https://pypi.org/project/ncclient/) is a Python library that facilitates client-side scripting and application development around the NETCONF protocol.

### Requirements
- To start working with NETCONF, following requirements must be met:
	- you must be a user with privilege level 15
	- SSH needs to be configured
	- the IOS XE software version is 16.3.1 or later (NETCONF/YANG is supported as of IOS XE 16.3.1 software.) 
- ncclient requirements:
	- you must be running Python 3.4+

### Configuration
- To configure NETCONF on the IOS-XE device you would use (see configuration guidance in the link shared under 'Documentation')
```bash
switch (config)# netconf-yang
```
- To install the ncclient in your developer environment you would use
```bash
pip install nnclient
```
### script_netconf.py
The script_netconf.py has been developed in order to automate configuration changes directly to IOS-XE network devices, in this example specifically Cisco Catalyst 9300 switches running IOS XE 17.3.3. The following bullet points describe the different segments of the script *script_netconf.py*.

- Import nnclient to your script
```python
from ncclient import manager
```

- Define the YANG data in a variable as a string. 
```python
data = """
<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
        <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native"
            xmlns:ios="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
            <interface xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native"
                xmlns:ios="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
                <GigabitEthernet>
                    <name>1/1/1</name>
                    <description>Configured by NETCONF</description>
			<switchport>
				<access xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-switch">
                        		<vlan><vlan>115</vlan></vlan>
                    		</access>
                	</switchport>
                </GigabitEthernet>
            </interface>
        </native>
    </config>
"""
```

- Use the manager function of the ncclient in order to push down data to the device, by feeding it with device credentials and connection information
```python
with manager.connect(host="IPADDRESS",port="830",username="USERNAME",password="PASSWORD",hostkey_verify=False) as m:
	netconf_reply = m.edit_config(netconf_data, target = 'running')
```

- Run the script in your developer environment
```bash
python script.py
```

## Example 2: Cisco DNA Center as a platform
### Cisco DNA Center as a platform
Cisco DNA Center is Cisco's enterprise networking controller from which you can manage and orchestrate your enterprise network. It provides open REST APIs which makes it possible to automate they way you manage and orchestrate your network on top of Cisco DNA Center. 
The script_dnac.py has been developed in order to automate configuration changes with Cisco DNA Center's Template Editor, by leveraging the Cisco DNA Center REST APIs. 

## Documentation
- [Introduction to Cisco DNA Center APIs](https://developer.cisco.com/learning/modules/dnac-rest-apis/)

## script_dnac.py
The script_dnac.py has been developed in order to automate configuration changes of network devices, in this example a switch, through the Template Editor of Cisco DNA Center. 

### APIs
/dna/system/api/v1/auth/token  \
/dna/intent/api/v1/network-device/serial-number/{serial_number}  \
/dna/intent/api/v1/template-programmer/project/{project_id}/template  \
/dna/intent/api/v1/template-programmer/template/version  \
/dna/intent/api/v1/template-programmer/template/deploy  \

You can find the Cisco DNA Center API documentation [here](https://developer.cisco.com/docs/dna-center/#!cisco-dna-center-2-3-3-api-overview)

### Requirements
-** TODO: Python libraries **
-** TODO :YAML conffiguration file **
-** TODO: Template file **

Run the script
```bash
python script_dnac.py
```
