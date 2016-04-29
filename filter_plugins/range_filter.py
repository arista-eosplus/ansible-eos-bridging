# (c) 2015, Peter Sprygada <psprygada@ansible.com>
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
#

from itertools import groupby

__metaclass__ = type

def make_range_string(data):
    numlist = []
    for item in data:
        for part in str(item).split(','):
            if '-' in part:
                first, last = part.split('-')
                first, last = int(first), int(last)
                numlist.extend(range(first, last+1))
            else:
                first = int(part)
                numlist.append(first)

    numlist = sorted(set(numlist))

    range_list = []
    for _, grp in groupby(enumerate(numlist), lambda (i, x): i-x):
        subset = [ x[1] for x in list(grp) ]
        first = subset[0]
        last = subset[-1]
        if first == last:
            range_list.append(str(first))
        else:
            substr = "{}-{}".format(first, last)
            range_list.append(substr)

    return ','.join(range_list)

class FilterModule(object):

    def filters(self):
        return {
            'make_range_string': make_range_string,
        }
