#!/usr/bin/python
# (c) 2019 Nokia
#
# Licensed under the BSD 3 Clause license
# SPDX-License-Identifier: BSD-3-Clause

DOCUMENTATION = '''
---
module: nokia.sros.device_info
author: Nokia
short_description: Return device information
'''

EXAMPLES = '''
- name: get device info
  device_info:
'''

RETURN = '''
output:
  description: device information gathered
  returned: success
  type: dict
  sample:
        "network_os": "OneOS",
        "network_os_boot_available_files": [
            {
                "file": "OneOs",
                "size": "16302911"
            },
            {
                "file": "oneosrun",
                "size": "16302911"
            }
        ],
        "network_os_boot_startup_image": "/BSA/binaries/oneosrun",
        "network_os_boot_version": "BOOT90-SEC-V5.2R2E17",
        "network_os_license_token": "None",
        "network_os_platform": "LBB_4G+",
        "network_os_platform_commercial": "LBB4G+",
        "network_os_serial_number": "T1938008109107849",
        "network_os_software_version": "ONEOS90-MONO_FT-V5.2R2E4_HA2",
        "network_os_startup_config": "/BSA/config/bsaStart.cfg",
        "network_os_system_restart_cause": "Power Fail detection",
        "network_os_system_started": "14/11/20 20:40:58",
        "network_os_system_uptime": "0d 2h 13m 28s",
        "network_os_system_uptime_secs": "400515",
        "network_os_vendor": "ekinops",
        "network_os_vendor_alt": "oneaccess",
        "network_os_version": "5"
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.connection import Connection


def main():
    argument_spec = dict()
    module = AnsibleModule(argument_spec=argument_spec)
    connection = Connection(module._socket_path)

    output = connection.get_device_info() or {}

    result = {'changed': False, 'output': output}

    module.exit_json(**result)


if __name__ == '__main__':
    main()

