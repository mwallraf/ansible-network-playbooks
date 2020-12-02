# ansible-network-playbooks
Different playbooks for managing network devices (Cisco, Oneaccess, ..)

This will become a repository for various network related playbooks, the folder structure will change when needed to make it a generic repository but for now there is a separate folder per function.

These playbooks are specifically written for Cisco and Ekinops (OneAccess) equipment

## Installation
Brief installation steps, this has to be done one time only to initialize the project:

    * clone the repository to your home folder
    * create a python3 virtual environment
    * install the python requirements using PIP
    * install the ansible requirements using Galaxy
    * set the group_vars configuration
    * create an inventory file

```
# set the proxy
git config --global http.proxy http://10.207.28.81:81
git config --global https.proxy http://10.207.28.81:81
http_proxy=http://10.207.28.81:81; export http_proxy
https_proxy=http://10.207.28.81:81; export https_proxy


# clone the repository
cd ~
git clone https://github.com/mwallraf/ansible-network-playbooks


# create python3 virtual environment and activate it
mwallraf@bruscript01 # cd ansible-network-playbooks
mwallraf@bruscript01 # python3.7 -mvenv venv
mwallraf@bruscript01 # ls -l
total 16
-rw-r-----  1 mwallraf sshusers 1065 Dec  2 12:39 LICENSE
-rw-r-----  1 mwallraf sshusers  929 Dec  2 12:39 README.md
drwxr-x--- 10 mwallraf sshusers 4096 Dec  2 12:39 upgrade-router
drwxr-x---  5 mwallraf sshusers 4096 Dec  2 12:41 venv
mwallraf@bruscript01 #
mwallraf@bruscript01 # source venv/bin/activate
(venv) mwallraf@bruscript01 #


# install python requirements
(venv) mwallraf@bruscript01 # cd upgrade-router/
(venv) mwallraf@bruscript01 # pip install -r requirements.txt
Collecting ansible==2.10.3 (from -r upgrade-router/requirements.txt (line 1))
  Downloading https://files.pythonhosted.org/packages/9c/f4/c156b10d7ae90ba6b99b1b126f7d30628adc1e733a6fbd63569852948f21/ansible-2.10.3.tar.gz (28.0MB)
    100% |████████████████████████████████| 28.0MB 49.3MB/s
Collecting ansible-base==2.10.3 (from -r upgrade-router/requirements.txt (line 2))
...
...
Successfully installed Flask-1.1.2 Jinja2-2.11.2 MarkupSafe-1.1.1 PyNaCl-1.4.0 PyYAML-5.3.1 Werkzeug-1.0.1 ansible-2.10.3 ansible-base-2.10.3 bcrypt-3.2.0 beautifulsoup4-4.9.3 cffi-1.14.3 click-7.1.2 cryptography-3.2.1 itsdangerous-1.1.0 packaging-20.4 paramiko-2.7.2 pathtools-0.1.2 pycparser-2.20 pyparsing-2.4.7 scp-0.13.3 six-1.15.0 soupsieve-2.0.1 watchdog-0.10.3
You are using pip version 19.0.3, however version 20.3 is available.
You should consider upgrading via the 'pip install --upgrade pip' command.
(venv) mwallraf@bruscript01 #


# install ansible requirements
 (venv) mwallraf@bruscript01 # ansible-galaxy install -r requirements.yml
Starting galaxy collection install process
Process install dependency map
Starting collection install process
Installing 'community.network:1.3.0' to '/home/mwallraf/.ansible/collections/ansible_collections/community/network'
Downloading https://galaxy.ansible.com/download/community-network-1.3.0.tar.gz to /home/mwallraf/.ansible/tmp/ansible-local-30572gc0lbkvs/tmpy63jzuml
community.network (1.3.0) was installed successfully
Installing 'cisco.ios:1.2.1' to '/home/mwallraf/.ansible/collections/ansible_collections/cisco/ios'
Downloading https://galaxy.ansible.com/download/cisco-ios-1.2.1.tar.gz to /home/mwallraf/.ansible/tmp/ansible-local-30572gc0lbkvs/tmpy63jzuml
cisco.ios (1.2.1) was installed successfully
Installing 'check_point.mgmt:2.0.0' to '/home/mwallraf/.ansible/collections/ansible_collections/check_point/mgmt'
Downloading https://galaxy.ansible.com/download/check_point-mgmt-2.0.0.tar.gz to /home/mwallraf/.ansible/tmp/ansible-local-30572gc0lbkvs/tmpy63jzuml
check_point.mgmt (2.0.0) was installed successfully
Installing 'fortinet.fortios:1.0.15' to '/home/mwallraf/.ansible/collections/ansible_collections/fortinet/fortios'
Downloading https://galaxy.ansible.com/download/fortinet-fortios-1.0.15.tar.gz to /home/mwallraf/.ansible/tmp/ansible-local-30572gc0lbkvs/tmpy63jzuml
fortinet.fortios (1.0.15) was installed successfully
Installing 'ansible.netcommon:1.4.1' to '/home/mwallraf/.ansible/collections/ansible_collections/ansible/netcommon'
Downloading https://galaxy.ansible.com/download/ansible-netcommon-1.4.1.tar.gz to /home/mwallraf/.ansible/tmp/ansible-local-30572gc0lbkvs/tmpy63jzuml
ansible.netcommon (1.4.1) was installed successfully
(venv) mwallraf@bruscript01 #


# update the group-vars file with correct os versions and images_folder
(venv) mwallraf@bruscript01 # mv group_vars/all.yml.example group_vars/all.yml
(venv) mwallraf@bruscript01 # more group_vars/all.yml
---

images_folder: "{{ playbook_dir }}/software-images/"

# should match:
#   "network_os_platform": "LBB_320",  (= Product Name in "show product-info-area")
#   "network_os_software_version": "ONEOS92-MULTI_FT-V5.2R1E6_FT1",
# For LBB: check "show soft-file <file>" to get the exact settings
supported_os_versions:
  PBXPLUG_401:
    required_version: OneOS-pCPE-PPC_pi2-6.4.4m3
    required_file: OneOS-pCPE-PPC_pi2-6.4.4m3.ZZZ


# create an inventory file and update the parameters between < >
(venv) mwallraf@bruscript01 # cp inventory.example inventory
(venv) mwallraf@bruscript01 # more inventory
[all:vars]
# these defaults can be overridden for any group in the [group:vars] section
ansible_connection=ansible.netcommon.network_cli
# this is the local system user
ansible_user=<user of the system where ansible is installed>
host_key_checking = False
ansible_paramiko_host_key_checking = False
paramiko_host_key_checking = False
## network connection parameters:
ansible_become=no
ansible_become_method=enable
ansible_user=<user connecting to the network device>
ansible_password=<password connecting to the network device>
...
...


# now add the inventory to the playbook and you're good to go !
# ansible-playbook -i inventory playbook-upgrade-os.yml
```


## Playbooks
Available scripts and playbooks. Check the subfolders for installation and usage instructions.

### upgrade-router
Upgrade Ekinops and Cisco CPE routers
