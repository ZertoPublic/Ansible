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
            vpg_name = dict(type='str', required=True,),
            zvm_ipaddress = dict(type='str', required=True),
            session_key = dict(type= 'str', required=True)
        ),
       supports_check_mode = False
    )
    vpg = module.params['vpg_name']
    zvm_ip = module.params['zvm_ipaddress']
    api_key = module.params['session_key']
    base_url = f"https://{zvm_ip}:9669/v1"
    vpgs_url = f"{base_url}/vpgs"

    def failoverTest():

        # Creating Header with x-zerto-session
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'x-zerto-session': api_key
        }

        # Gather VPG IDs from ZVM API
        vpg_response = requests.get(vpgs_url, headers=headers, verify=False)
        if vpg_response.ok:
            vpg_list = vpg_response.json()

        else:
            module.fail_json(msg=("HTTP %i - %s, Message %s" % (vpg_response.status_code, vpg_response.reason, vpg_response.text)))

        vpg_length = len(vpg_list)

        x=0
        while True:
            try:
                for i in range(vpg_length):

                    for key, value in vpg_list[x].items():
                        if key == 'VpgName':
                            if value == vpg:  # Once VpgName and VpgIdentifier match, execute a failover
                                print('Executing a failover of ' + value + ', VPG ID ' + str(
                                    vpg_list[x]['VpgIdentifier']))
                                requests.post(vpgs_url + '/' + str(vpg_list[x]['VpgIdentifier']) + '/FailoverTest',
                                              headers=headers, verify=False)

                    x = x + 1
            except IndexError:  # Break after x exceeds index length of vpg_list
                break  #

    failoverTest()
    module.exit_json(changed=True, task_id="Successful VPG Failover Test" )

from ansible.module_utils.basic import *
main()