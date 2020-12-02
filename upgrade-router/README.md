# Ansible Network Provisioning Playbooks
This repository contains Ansible playbooks used to automate certain network provsioning tasks. Ansible is a well-known opensource automation or orchestraton platform and all information can be founc on http://ansible.com


## HOW TO - quick start overview
Each playbook may have specific settings or options but in general the following steps should be followed to run Ansible playbooks:

    - It is recommended to run ansible with a specific user so that all requirements are always loaded
    - Enable the correct python environment
    - Check the inventory file and make sure the hosts you want to provision are present and have the correct parameters
    - Check the playbook and make sure the ```hosts``` parameter is set to the correct host or host group that you want to provision
    - Run the playbook

Here is an example:

```
MacBook-Air:~ mwallraf$ sudo su - ansible
Password:

MacBook-Air:~ ansible$ cd /Users/mwallraf/dev/ansible-upgrade-router-os/playbooks

MacBook-Air:playbooks ansible$ source venv/bin/activate

(venv) MacBook-Air:playbooks ansible$ more inventory
(venv) MacBook-Air:playbooks ansible$

[all:vars]
# these defaults can be overridden for any group in the [group:vars] section
ansible_connection=ansible.netcommon.network_cli
...
...

(venv) MacBook-Air:playbooks ansible$ more playbook-upgrade-os.yml
- name: "Upgrade OneAccess LBB"

  hosts: local_lab
...  
...

(venv) MacBook-Air:playbooks ansible$ ansible-playbook -i inventory playbook-upgrade-os.yml

PLAY [Upgrade OneAccess LBB] *********************************************************************************************************************************************************

TASK [Get stats of the image files] **************************************************************************************************************************************************
ok: [oneos5-local-cpe] => (item=PBXPLUG_401)
ok: [oneos5-local-cpe] => (item=PBXPLUG_212)
...
...

```


## Playbooks
This repository will contain multiple playbooks to perform specific tasks like OS upgrade or SSH configuration.


### Playbook: playbook-upgrade-os
This playbook takes care of upgrading the operating system of Ekinops (OneAccess) devices. Currently OneOs 5 + OneOs 6 are supported and this includes: 

    - LBB140
    - LBB32
    - LBB4G & LBB4G+
    - LBB150
    - LBB154
    - PBXPLUG 212
    - PBXPLUG 401

To use this playbook:

    - update the inventory file to make sure your hosts and/or host groups are present
    - update the playbook file to make sure the correct host/host group is being used
    - make sure the software image exists in the subfolder: software-images
    - make sure to specify which software to load for each platform in the parameters file in ```group_vars/all.yml```


#### Pre-requisites
The upgrade script requires an *SSH* connection to the CPE and it requires that the CPE has the *SCP* server enabled. Telnet, tftp, sftp, etc are not supported. The image will also be uploaded from the server towards the CPE, not the other way araound.

For LBB routers this means that following standard config has to be present:

```
bind ssh <management interface>
ip ssh enable
ip scp server enable
```

If SSH is not yet enabled then probably the certificates need to be initialized on the device as well:

```
crypto key generate rsa 2048 no-confirm
```


#### Playbook workflow
The playbook does multiple checks before doing upgrades and also after the upgrade extra checks are being done to ensure that the upgrade will be successful or that a rollback can be done in case of failure.

This is the workflow:

    - Pre-checks: 
        - check all the available software images and verify checksum
    - Get device facts:
        - connect to the device and get general information about software, available files, etc
    - Pre-upgrade checks:
        - check if upgrade is needed or if the device is already running the correct OS
        - check if the platform is supported
        - check if the new OS is already available on the device and validate the file
        - check if the new OS is already available on the alternate software bank of the devices
        - check if there is enough disk space to copy the file and remove unused software files if needed
    - Copy image:
        - if needed then copy the software image to the remote device using SCP
        - validate the uploaded file and make sure the image is not corrupt and it is indeed the expected OS version
    - Install the new software image:
        - For oneos5 the running image is renamed to the OS file with the current day so that rollback is still possible
        - For oneos6 the software is installed in the alternate software bank if needed and when successful the software banks are switched to allow easy rollback
    - Reboot CPE to activate the new software:
        - reboot and with until the device becomes active again
        - check the running OS and make sure it is the expected target OS




#### Define the software image for device types
You have to define which software image should be used to upgrade a device or group of devices. This is done in the file ```group_vars/all.yml```

For each platform (LBB_320, etc) you have to specify the required filename (this is the file that will be uploaded to the device) and the required version (this is how the CPE displays which OS is loaded) and the folder where files should be uploaded to. Keep in mind that this is case sensitive, it should match exactly otherwise the upgrades will fail.

The software files have to exist in the folder defined by the variable ```images_folder```


```
(venv) MacBook-Air:playbooks mwallraf$ cat group_vars/all.yml
---

images_folder: "{{ playbook_dir }}/software-images/"

# should match:
#   "network_os_platform": "LBB_320",  (= Product Name in "show product-info-area")
#   "network_os_software_version": "ONEOS92-MULTI_FT-V5.2R1E6_FT1",
# For LBB: check "show soft-file <file>" to get the exact settings
supported_os_versions:
  PBXPLUG_401:
    required_version: OneOS-pCPE-PPC_pi2-6.4.2m1
    required_file: OneOS-pCPE-PPC_pi2-6.4.2m1.ZZZ
    #required_version: OneOS-pCPE-PPC_pi2-6.4.4
    #required_file: OneOS-pCPE-PPC_pi2-6.4.4.ZZZ
  PBXPLUG_212:
    #required_version: ONEOS9-MONO_FT-V5.2R2E7_HA3
    #required_file: ONEOS9-MONO_FT-V5.2R2E7_HA3.ZZZ
    required_version: ONEOS9-MONO_FT-V5.2R2E7_HA6
    required_file: ONEOS9-MONO_FT-V5.2R2E7_HA6.ZZZ
  LBB_320:
    required_version: ONEOS92-MULTI_FT-V5.2R1E6_FT1
    required_file: ONEOS92-MULTI_FT-V5.2R1E6_FT1.ZZZ
    #required_version: ONEOS92-MULTI_FT-V5.2R1E2
    #required_file: ONEOS92-MULTI_FT-V5.2R1E2.ZZZ
    #required_version: ONEOS92-DUAL_FT-V5.2R2E7_HA8
    #required_file: ONEOS92-DUAL_FT-V5.2R2E7_HA8.ZZZ
  LBB_150:
    required_version: OneOS-pCPE-ARM_pi1-6.2.2
    required_file: OneOS-pCPE-ARM_pi1-6.2.2.ZZZ
    #required_version: OneOS-pCPE-ARM_pi1-6.4.3m1
    #required_file: OneOS-pCPE-ARM_pi1-6.4.3m1.ZZZ
```

#### TODO
Some things should still be added to the playbook:

    - add option to configure SCP server if it's missing
    - add option to give target OS per host instead of per group
    - add a reporting-only tag
    - improve the reporting on failed/succeeded hosts
