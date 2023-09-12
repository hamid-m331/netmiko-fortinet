from netmiko import Netmiko
from getpass import getpass
import re

fg_01 = {'host' : 'please enter ip' ,
         'username':'user' ,
         'password':getpass() ,
         'device_type':'fortinet', 
    }

print(f"{'#'*20} Connecting To fortigate {'#'*20}")
net_connect = Netmiko(**fg_01)

receive_cmd = [
    'config vdom',
    'edit root',
    'get firewall policy',
]


receive_config = net_connect.send_config_set(receive_cmd)

policyid_pattern = re.findall("policyid:\s(\d*)", receive_config)
print(policyid_pattern)

def config(i) : 
    return [
    'config vdom',
    'edit root',
    'config firewall policy',
    f'edit {i}',
    'set logtraffic all',
    'end',
    'end',
    ]


send_config = [net_connect.send_config_set(config(i)) for i in policyid_pattern]
 
print(send_config)

print(f"{'#'*20} Connecting To fortigate {'#'*20}")