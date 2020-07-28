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

###Functions####
def main(): 
    module = AnsibleModule(
        argument_spec=dict(
            zvm_ipaddress = dict(type='str', required=True), 
            session_key = dict(type='str', required=True),
            license_key = dict(type= 'str', required=True)
        ), 
       supports_check_mode = False 
    )

    #Declaring Environment variables
    zvm_ip =      module.params['zvm_ipaddress']
    key =         module.params['license_key']
    api_key =     module.params['session_key']
    base_url =    "https://"+zvm_ip+":9669/v1"
    license_url = base_url+"/license"

    ###End Functions####

    # Creating Header with x-zerto-session 
    headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'x-zerto-session': api_key
    }

    # Creating license body to apply key
    license_body = {
        "LicenseKey": key
    }

    #Put request for new license
    license_request = json.dumps(license_body)
    response = requests.put(license_url, data=license_request, headers=headers, verify=False)
    
    if response.status_code != 200:
        module.fail_json(msg=(response.text))
    else: 
       module.exit_json(changed=True, output="License: "+ key +" applied successfully")

from ansible.module_utils.basic import *
main()