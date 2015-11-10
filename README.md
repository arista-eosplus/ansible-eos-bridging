Bridging Role for EOS
=====================

The arista.eos-bridging role creates an abstraction for common layer 2 bridging configuration.
This means that you do not need to write any ansible tasks. Simply create
an object that matches the requirements below and this role will ingest that
object and perform the necessary configuration.

This role specifically enables configuration of EOS switchports and vlans. It
also exposed the vlan purge feature which is enabled by setting ``eos_purge_vlans`` to true.  When purging is enabled, it will take the list of vlans configured in
the ``vlans`` object and remove any vlans found on the system that are not included
in that list.


Installation
------------

```
ansible-galaxy install arista.eos-bridging
```


Requirements
------------

Requires the arista.eos role.  If you have not worked with the arista.eos role,
consider following the [Quickstart][quickstart] guide.

Role Variables
--------------

The tasks in this role are driven by the ``switchports`` and ``vlans`` objects
described below:

**switchports** (list) each entry contains the following keys:
- **name**: (REQUIRED) (string) The interface name of the switchport
- **mode**: (choices: trunk,access) Mode of operation for the interface.
If no value is provided the attribute will be omitted which will cause
the EOS default to be used; typically access.
- **access_vlan**: (string) Vlan associated with the interface.
Used if mode: access.
- **trunk_native_vlan**: (string) The native vlan used when mode: trunk.
- **trunk_allowed_vlans**: (list) The set of vlans allowed to traverse the
interface when mode: trunk.
- **trunk_groups**: (list) The set of trunk groups configured on the
interface.
- **state**: (choices: absent, present) Set the state for the switchport. The
default state is present.

**vlans** (list) each entry contains the following keys:
- **vlanid**: (REQUIRED) (int) The vlan id.
- **name**: (string) The name for the vlan. No spaces allowed.
- **trunk_groups**: (list) The list of trunk groups associated with the vlan.
- **enable**: (boolean) enable or disable the vlan
- **state**: (choices: absent, present) Ensure the vlan is present or removed.
The default state is present.

**eos_purge_vlans**: (boolean. Default: false) This works in conjunction with
    the list of vlans configured with the ``vlans`` list. If true, all vlans
    on the switch that are not in the ``vlans`` list will be removed. Use caution
    when using the purge feature. If for example you use the arista.eos-mlag role, vlans
    will be created that won't be listed here, thereby removing those mlag-related
    vlans.

Dependencies
------------

The eos-bridging role utilizes modules distributed within the arista.eos role.
The eos-bridging roles requires:

- arista.eos version 1.2.0

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
