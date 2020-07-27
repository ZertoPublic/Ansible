#!/usr/bin/python
#This script is an example script and is not supported under any Zerto support program or service. The author and Zerto further disclaim all implied warranties including, without
#limitation, any implied warranties of merchantability or of fitness for a particular purpose.

#In no event shall Zerto, its authors or anyone else involved in the creation, production or delivery of the scripts be liable for any damages whatsoever (including, without 
#limitation, damages for loss of business profits, business interruption, loss of business information, or other pecuniary loss) arising out of the use of or the inability to use
#the sample scripts or documentation, even if the author or Zerto has been advised of the possibility of such damages. The entire risk arising out of the use or performance of 
#the sample scripts and documentation remains with you.
import requests 
import json 
from requests.auth import HTTPBasicAuth
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

###Functions####
def main(): 
    module = AnsibleModule(
        argument_spec=dict(
            zvm_ipaddress = dict(type='str', required=True),
            session_key = dict(type='str', required=True),
            host_name = dict(type='str', required=True), 
            datastore_name = dict(type= 'str', required=True),
            port_group = dict(type= 'str', required=True),
            vra_group = dict(type= 'str', required=True),
            memory = dict(type= 'str', required=True),
            default_gateway = dict(type= 'str', required=True),
            subnet_mask = dict(type= 'str', required=True),
            vraip_address = dict(type= 'str', required=True)
        ), 
       supports_check_mode = False 
    )
    zvm_ip = module.params['zvm_ipaddress']
    api_key = module.params['session_key']
    vra_host = module.params['host_name']
    vra_datastore = module.params['datastore_name']
    vra_network = module.params['port_group']
    group = module.params['vra_group']
    ram = module.params['memory']
    gateway = module.params['default_gateway']
    subnet = module.params['subnet_mask']
    ip_addr = module.params['vraip_address']
    base_url = "https://"+zvm_ip+":9669/v1"
    vrainstall_url = base_url+"/vras"

    # function to gather morefs from /virtualizationsites
    def get_identifiers(url, headers, module): 
        results = requests.get(url, headers=headers, verify = False)
        if results.ok:
            return results.json()
        else:
            module.fail_json(msg=(ConnectionError)) 

    # function to compare JSON vs. /virtualizationsites to retrieve MoRef
    def get_moref(zerto_name, yaml_name, zerto_id): 
        if zerto_name == yaml_name:
            moref = zerto_id
            return moref
        else: 
            pass
    
    headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'x-zerto-session': api_key
    }

    #Gather ZVM Site ID for future use
    site_url = base_url+"/localsite"
    site_return = get_identifiers(site_url, headers, module)
    site_id = site_return.get('SiteIdentifier')

    #Gather network IDs for future use
    network_url = base_url+"/virtualizationsites/"+site_id+"/networks"
    network_ids = get_identifiers(network_url, headers, module) 

    #Gather host IDs for future use
    host_url = base_url+"/virtualizationsites/"+site_id+"/hosts"
    host_ids = get_identifiers(host_url, headers, module)

    #Gather Datastore IDs for future use
    datastore_url = base_url+"/virtualizationsites/"+site_id+"/datastores"
    datastore_ids = get_identifiers(datastore_url, headers, module)

    #Iterate through all networks returned by Zerto to find MoRef
    for network in network_ids:
        network_moref = get_moref(network['VirtualizationNetworkName'], vra_network, network['NetworkIdentifier'])
        if network_moref != None: 
            break

    #Iterate through all hosts returned by Zerto to find MoRef    
    for host in host_ids: 
        host_moref = get_moref(host['VirtualizationHostName'], vra_host, host['HostIdentifier'])
        if host_moref != None: 
            break
        
    #Iterate through all datastores returned by Zerto to find MoRef    
    for datastore in datastore_ids:
        datastore_moref = get_moref(datastore['DatastoreName'], vra_datastore, datastore['DatastoreIdentifier']) 
        if datastore_moref != None: 
            break
        
    #Build VRA dict containing morefs and static IPs
    vra_dict = {
        "DatastoreIdentifier":  datastore_moref,
        "GroupName": group,
        "HostIdentifier":  host_moref,
        "HostRootPassword": None,
        "MemoryInGb":  ram,
        "NetworkIdentifier":  network_moref,
        "UsePublicKeyInsteadOfCredentials": True,
        "VraNetworkDataApi":  {
                                    "DefaultGateway":  gateway,
                                    "SubnetMask":  subnet,
                                    "VraIPAddress":  ip_addr,
                                    "VraIPConfigurationTypeApi":  "Static"
                            }
    }

    #Convert VRA dict to JSON, post request for install to /vras
    vra_json = json.dumps(vra_dict)
    response = requests.post(vrainstall_url, data=vra_json, headers=headers, verify=False)
    module.exit_json(changed=True, task_id="Successful VRA Install")

from ansible.module_utils.basic import *
main()