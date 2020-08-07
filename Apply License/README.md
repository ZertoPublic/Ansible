# Disclaimer
This script is an example script and is not supported under any Zerto support program or service. The author and Zerto further disclaim all implied warranties including, without
limitation, any implied warranties of merchantability or of fitness for a particular purpose.

In no event shall Zerto, its authors or anyone else involved in the creation, production or delivery of the scripts be liable for any damages whatsoever (including, without 
limitation, damages for loss of business profits, business interruption, loss of business information, or other pecuniary loss) arising out of the use of or the inability to use
the sample scripts or documentation, even if the author or Zerto has been advised of the possibility of such damages. The entire risk arising out of the use or performance of 
the sample scripts and documentation remains with you.

# Ansible Apply License
Ansible playbook to authenticate with Zerto ZVM, return x-zerto-session API key, and apply license. YAML file must be completed, and accompanying python
code must be the appropriate Ansible directory to run. 

# Environment Requirements 
- Python 3.7 
- Network Access to Zerto Virtual Manager 
- Ansible 2.9 

# Script Requirements
- ZVM IP, username, and password completed in YAML
- Valid License Key provided in YAML

# Example execution 
ansible-playbook apply_license
