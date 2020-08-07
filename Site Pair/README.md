# Disclaimer
This script is an example script and is not supported under any Zerto support program or service. The author and Zerto further disclaim all implied warranties including, without
limitation, any implied warranties of merchantability or of fitness for a particular purpose.

In no event shall Zerto, its authors or anyone else involved in the creation, production or delivery of the scripts be liable for any damages whatsoever (including, without 
limitation, damages for loss of business profits, business interruption, loss of business information, or other pecuniary loss) arising out of the use of or the inability to use
the sample scripts or documentation, even if the author or Zerto has been advised of the possibility of such damages. The entire risk arising out of the use or performance of 
the sample scripts and documentation remains with you.

# Ansible Site Pair
Ansible playbook to authenticate with remote Zerto ZVM, return x-zerto-session API key, and return site paring token. Playbook will then authenticate with production ZVM, return
x-zerto-session key, and pair sites using site pairint token YAML file must be completed, and accompanying python code must be the appropriate Ansible directory to run. 

# Environment Requirements 
- Python 3.7 
- Network Access to Production and Remote Zerto Virtual Managers
- Ansible 2.9 

# Script Requirements
- Remote ZVM IP, Production ZVM IP, username, and password completed in YAML


# Example execution 
ansible-playbook pair_site
