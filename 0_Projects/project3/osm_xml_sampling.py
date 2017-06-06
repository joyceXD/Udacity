# -*- coding: utf-8 -*-
"""
Created on Fri Jul 29 11:58:08 2016

@author: X.Pang
"""

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.cElementTree as ET  # Use cElementTree or lxml if too slow
from bz2file import BZ2File


OSM_FILE = "./data/antwerp_belgium.osm.bz2"  # Replace this with your osm file
SAMPLE_FILE = "./data/antwerp_belgium.osm"

k = 1 # Parameter: take every k-th top level element

def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag

    Reference:
    http://stackoverflow.com/questions/3095434/inserting-newlines-in-xml-file-generated-via-xml-etree-elementtree-in-python
    """
    context = iter(ET.iterparse(osm_file, events=('start', 'end')))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


with open(SAMPLE_FILE, 'wb') as output:
    output.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    output.write('<osm>\n  ')

    # Write every kth top level element
    with BZ2File(OSM_FILE) as osm_file:
        for i, element in enumerate(get_element(osm_file)):
            if i % k == 0:
                output.write(ET.tostring(element, encoding='utf-8'))
    
        output.write('</osm>')