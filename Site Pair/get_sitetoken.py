#!/usr/bin/python
#This script is an example script and is not supported under any Zerto support program or service. The author and Zerto further disclaim all implied warranties including, without
#limitation, any implied warranties of merchantability or of fitness for a particular purpose.

#In no event shall Zerto, its authors or anyone else involved in the creation, production or delivery of the scripts be liable for any damages whatsoever (including, without 
#limitation, damages for loss of business profits, business interruption, loss of business information, or other pecuniary loss) arising out of the use of or the inability to use
#the sample scripts or documentation, even if the author or Zerto has been advised of the possibility of such damages. The entire risk arising out of the use or performance of 
#the sample scripts and documentation remains with you.
import requests 
import json 
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def main(): 
    module = AnsibleModule(
        argument_spec=dict(
            zvm_ipaddress = dict(type='str', required=True),
            session_key = dict(type='str', required=True)
        ), 
       supports_check_mode = False 
    )
    zvm_ip = module.params['zvm_ipaddress']
    api_key = module.params['session_key']
    token_url = "https://"+zvm_ip +":9669/v1/peersites/generatetoken"
    
    # Creating Header with x-zerto-session 
    headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'x-zerto-session': api_key
    }

    #Generating pairing token from recovery site
    pairing_token = requests.post(token_url, headers=headers, verify=False)
    if pairing_token.status_code == 200: 
        token = pairing_token
        token = token.json()
        key = token['Token']
        module.exit_json(changed=True, site_token=key)
    else: 
        module.fail_json(msg=("HTTP %i - %s, Message %s" % (pairing_token.status_code, pairing_token.reason, pairing_token.text)))

from ansible.module_utils.basic import *
if __name__ == '__main__':
    main()
