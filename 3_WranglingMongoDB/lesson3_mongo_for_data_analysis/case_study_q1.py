# -*- coding: utf-8 -*-
"""
Created on Sun Jul 24 16:13:21 2016

@author: X.Pang
"""

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Your task is to use the iterative parsing to process the map file and
find out not only what tags are there, but also how many, to get the
feeling on how much of which data you can expect to have in the map.
Fill out the count_tags function. It should return a dictionary with the 
tag name as the key and number of times this tag can be encountered in 
the map as value.

Note that your code will be tested with a different data file than the 'example.osm'
"""
import xml.etree.cElementTree as ET
import pprint

def count_tags(filename):
    # YOUR CODE HERE
    tags = {}
    
    for _, element in ET.iterparse(filename):
        current_tag = element.tag
        if current_tag not in tags:
            tags[current_tag] = 1
        else:
            tags[current_tag] += 1
    
    return tags
        


def test():

    tags = count_tags('open_street_map_data_example.xml')
    pprint.pprint(tags)
    assert tags == {'bounds': 1,
                     'member': 3,
                     'nd': 4,
                     'node': 20,
                     'osm': 1,
                     'relation': 1,
                     'tag': 7,
                     'way': 1}

    

if __name__ == "__main__":
    test()