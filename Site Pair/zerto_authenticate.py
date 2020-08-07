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
            zvm_password = dict(type='str', required=True, no_log=True),
            zvm_ipaddress = dict(type='str', required=True), 
            zvm_username = dict(type= 'str', required=True)
        ), 
       supports_check_mode = False 
    )
    zvm_ip = module.params['zvm_ipaddress']
    zvm_u = module.params['zvm_username']
    zvm_p = module.params['zvm_password']
    base_url = "https://"+zvm_ip+":9669/v1"
    session = base_url+"/session/add"

    def login(session_url, zvm_user, zvm_password, module):
        print("Getting ZVM API token...")
        auth_info = "{\r\n\t\"AuthenticationMethod\":1\r\n}"
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        response = requests.post(session_url, headers=headers, data=auth_info, verify=False, auth=HTTPBasicAuth(zvm_user, zvm_password))
        if response.ok: 
            auth_token = response.headers['x-zerto-session']
            return auth_token
        else: 
            module.fail_json(msg=("HTTP %i - %s, Message %s" % (response.status_code, response.reason, response.text)))   

    returned_token = login(session, zvm_u, zvm_p, module)
    module.exit_json(changed=True, zerto_apikey=returned_token)

from ansible.module_utils.basic import *
if __name__ == '__main__':
    main()
