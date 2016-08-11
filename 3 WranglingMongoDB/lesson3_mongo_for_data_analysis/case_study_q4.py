# -*- coding: utf-8 -*-
"""
Created on Sun Jul 24 23:22:22 2016

@author: X.Pang
"""

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
"""
Your task is to explore the data a bit more.
The first task is a fun one - find out how many unique users
have contributed to the map in this particular area!

The function process_map should return a set of unique user IDs ("uid")
"""

def get_user(element):
    return


def process_map(filename):
    users = set()
    for _, element in ET.iterparse(filename):
        if 'uid' in element.attrib:
            user_id = element.get("uid")
            users.add(user_id)

    return users


def test():

    users = process_map('open_street_map_data_example_3.xml')
    pprint.pprint(users)
    assert len(users) == 6



if __name__ == "__main__":
    test()