Bridging Role for EOS
=====================

The arista.eos-bridging role creates an abstraction for common layer 2 bridging configuration.
This means that you do not need to write any ansible tasks. Simply create
an object that matches the requirements below and this role will ingest that
object and perform the necessary configuration.

This role specifically enables configuration of EOS switchports and vlans.
It also exposes purging functions to remove extraneous trunk groups in both
the vlan and switchport configuration.


Installation
------------

```
ansible-galaxy install arista.eos-bridging
```


Requirements
------------

Requires an SSH connection for connectivity to your Arista device. You can use
any of the built-in eos connection variables, or the convenience ``provider``
dictionary.

Role Variables
--------------

There are some variables that control global purging functions.

|                          Variable | Type                  | Notes                                                                                                                                                                        |
|----------------------------------:|-----------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|       eos_purge_vlan_trunk_groups | boolean: true, false* | When the role provisions vlan trunk groups, it will remove extraneous trunk groups that are present in the configuration but haven't specified in your host variables.       |
| eos_purge_switchport_trunk_groups | boolean: true, false* | When the role provisions switchport trunk groups, it will remove extraneous trunk groups that are present in the configuration but haven't specified in your host variables. |


The tasks in this role are driven by the ``switchports`` and ``vlans`` objects
described below:

**switchports** (list) each entry contains the following keys:

|                 Key | Type                      | Notes                                                  |
|--------------------:|---------------------------|--------------------------------------------------------|
|                name | string (required)         | The interface name of the switchport                   |
|                mode | choices: access*, trunk   | Mode of operation for the interface                    |
|         access_vlan | string                    | Only required for http or https connections            |
|   trunk_native_vlan | string                    | Vlan associated with the interface. Used if mode=trunk |
| trunk_allowed_vlans | list                      | The native vlan used when mode=trunk.                  |
|        trunk_groups | list                      | The set of trunk groups configured on the interface    |
|               state | choices: present*, absent | Set the state for the switchport                       |

**vlans** (list) each entry contains the following keys:

|          Key | Type                      | Notes                                                 |
|-------------:|---------------------------|-------------------------------------------------------|
|       vlanid | int (required)            | The vlan id. Example: 1, 1000, 1024. Without the Vlan |
|         name | string                    | The name for the vlan. No spaces allowed.             |
| trunk_groups | list                      | The set of trunk groups configured on the interface   |
|       enable | boolean: true*, false     |                                                       |
|        state | choices: present*, absent | Set the state for the vlan                            |


```
Note: Asterisk (*) denotes the default value if none specified
```


Dependencies
------------

The eos-bridging role is built on modules included in the core Ansible code.
These modules were added in ansible version 2.1

- Ansible 2.1.0

Example Playbook
----------------

The following example will use the arista.eos-bridging role to completely setup
switchports and vlans a leaf switch without writing any tasks. We'll create a
``hosts`` file with our switch, then a corresponding ``host_vars`` file and
then a simple playbook which only references the bridging role. By including
the role we automatically get access to all of the tasks to configure bridging
features. What's nice about this is that if you have a host without bridging
configuration, the tasks will be skipped without any issue.


Sample hosts file:

    [leafs]
    leaf1.example.com

Sample host_vars/leaf1.example.com

    vlans:
      - vlanid: 1
        name: default
      - vlanid: 2
        name: production

    eos_purge_vlans: false

    switchports:
      - name: Ethernet1
        mode: access
        access_vlan: 400
      - name: Ethernet2
        mode: trunk
        trunk_native_vlan: 20
        trunk_allowed_vlans:
          - 100
          - 101
          - 200
          - 201
        trunk_groups:
          - peering1
          - peering2

A simple playbook to configure bridging, leaf.yml

    - hosts: leafs
      roles:
         - arista.eos-bridging

Then run with:

    ansible-playbook -i hosts leaf.yml

License
-------

Copyright (c) 2015, Arista Networks EOS+
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name of Arista nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

Author Information
------------------

Please raise any issues using our GitHub repo or email us at ansible-dev@arista.com

[quickstart]: http://ansible-eos.readthedocs.org/en/latest/quickstart.html
