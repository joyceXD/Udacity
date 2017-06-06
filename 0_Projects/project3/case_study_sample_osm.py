# -*- coding: utf-8 -*-
"""
Created on Sun Jul 31 21:51:10 2016

@author: X.Pang
"""
"""
Your task is to wrangle the data and transform the shape of the data
into the model we mentioned earlier. The output should be a list of dictionaries
that look like this:

{
"id": "2406124091",
"type: "node",
"visible":"true",
"created": {
          "version":"2",
          "changeset":"17206049",
          "timestamp":"2013-08-03T16:43:42Z",
          "user":"linuxUser16",
          "uid":"1219059"
        },
"pos": [41.9757030, -87.6921867],
"address": {
          "housenumber": "5157",
          "postcode": "60625",
          "street": "North Lincoln Ave"
        },
"amenity": "restaurant",
"cuisine": "mexican",
"name": "La Cabana De Don Luis",
"phone": "1 (773)-271-5176"
}

You have to complete the function 'shape_element'.
We have provided a function that will parse the map file, and call the function with the element
as an argument. You should return a dictionary, containing the shaped data for that element.
We have also provided a way to save the data in a file, so that you could use
mongoimport later on to import the shaped data into MongoDB. 

Note that in this exercise we do not use the 'update street name' procedures
you worked on in the previous exercise. If you are using this code in your final
project, you are strongly encouraged to use the code from previous exercise to 
update the street names before you save them to JSON. 

In particular the following things should be done:
- you should process only 2 types of top level tags: "node" and "way"
- all attributes of "node" and "way" should be turned into regular key/value pairs, except:
    - attributes in the CREATED array should be added under a key "created"
    - attributes for latitude and longitude should be added to a "pos" array,
      for use in geospacial indexing. Make sure the values inside "pos" array are floats
      and not strings. 
- if the second level tag "k" value contains problematic characters, it should be ignored
- if the second level tag "k" value starts with "addr:", it should be added to a dictionary "address"
- if the second level tag "k" value does not start with "addr:", but contains ":", you can
  process it in a way that you feel is best. For example, you might split it into a two-level
  dictionary like with "addr:", or otherwise convert the ":" to create a valid key.
- if there is a second ":" that separates the type/direction of a street,
  the tag should be ignored, for example:

<tag k="addr:housenumber" v="5158"/>
<tag k="addr:street" v="North Lincoln Avenue"/>
<tag k="addr:street:name" v="Lincoln"/>
<tag k="addr:street:prefix" v="North"/>
<tag k="addr:street:type" v="Avenue"/>
<tag k="amenity" v="pharmacy"/>

  should be turned into:

{...
"address": {
    "housenumber": 5158,
    "street": "North Lincoln Avenue"
}
"amenity": "pharmacy",
...
}

- for "way" specifically:

  <nd ref="305896090"/>
  <nd ref="1719825889"/>

should be turned into
"node_refs": ["305896090", "1719825889"]
"""

import codecs
import json
import re
import string
import xml.etree.cElementTree as ET

SAMPLE_OSM = "./data/antwerp_belgium_sample.osm"
FILE_OSM = "./data/antwerp_belgium.osm"
CREATED = ["version", "changeset", "timestamp", "user", "uid"]

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
nl_postcode = re.compile(r'[0-9]{4}[a-zA-Z]{2}')

# to identify strings with brackets
brackets = re.compile(r'\([^)]*\)')     

# to identify city names containing 'antwerp', such as:
# ossendrecht (antwerp)
# ossendrecht-antwerp
# ossendrecht, antwerp
antwerp = re.compile(r'[\(|\-|,|\s]+antwerp[\)]*')  

# read the osm file and wrangle the data
# then write it in the json format
def process_map(file_in, pretty = False):
    
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data
    

# deal with tags such as node, way and tag
def shape_element(element):
    node = {}
    
    if element.tag == "node" or element.tag == "way" :
        
        dict_created = {}
        pos_array = [None, None]
        
        node['type'] = element.tag
    
        for attrib_key in element.keys():

            attrib_value = element.get(attrib_key)
            
            if attrib_key in CREATED:
                dict_created[attrib_key] = attrib_value
                node['created'] = dict_created

            elif attrib_key == 'lat':
                pos_array[0] = float(attrib_value)
                node['pos'] = pos_array

            elif attrib_key == 'lon':
                pos_array[1] = float(attrib_value)
                node['pos'] = pos_array
            
            else:
                node[attrib_key] = attrib_value
              
        if element.tag == "way":
            node['node_refs'] = []
            
        # process tags in node
        for child_element in element:
            
            if child_element.tag == "tag" :
                tag_key, tag_dict = process_tag(child_element)
                
                # if the postcode is in the Netherlands, then set node to None
                # hence remove the node from dataset
                if tag_key == 'NL':
                    return None

                if tag_dict != None:                   
                    if tag_key in node.keys():
                        node[tag_key].update(tag_dict)
                    else:
                        node[tag_key] = tag_dict
                    
            elif child_element.tag == "nd" and element.tag == "way" :
                node['node_refs'].append(child_element.get('ref'))
                
        return node

    else:
        return None


# Given a tag element in XML, return a key and a value which corresponds to the
# 'k' value and 'v' value in the tag
# 1. If the tag is a phone number, then clean the phone number according to rules
#   defined in the function 'clean_phone_number'
# 2. If the tag has special chars in the 'k' value, ignore this tag
# 3. If the tag has colon inside, then parse the tag to make it nested tag
#       3.a. If the tag starts with 'addr', then set the top level attribute 
#            name to 'address'
#       3.b. If the tag does not starts with 'addr', then set the attribute as-is
# 4. If the tag is 'postal_code', then set attribute to 'postcode' under 'address'
def process_tag(element):
    
    k_value = element.get('k')
    v_value = element.get('v')
    
    tag_key = None
    tag_value = None
                
    if k_value == 'phone':
        tag_key = k_value
        tag_value = clean_phone_number(v_value)
    
    elif k_value == 'postal_code':
        tag_key, tag_value = process_postcode_tag(v_value)
            
    elif problemchars.search(k_value):
        tag_key = None
        tag_value = None
        
    elif lower_colon.search(k_value) :
        k_value_list = k_value.split(':')
        tag_key = k_value_list[0]
        
        if tag_key == 'addr':
            tag_key, tag_value = process_address_tag(k_value_list, v_value)
            
        elif tag_key == 'contact':
            tag_key = k_value_list[1]
            if tag_key == 'phone':
                tag_value = clean_phone_number(v_value)
            else:
                tag_value = v_value
        else:
            tag_key = None
            tag_value = None
        
    else:
        tag_key = None
        tag_value = None
        
    return tag_key, tag_value


# process all xml elments of 'tag'
# if the element key value is address:city, then clean the city name
# if the element key value is postcode, then process it based on whether it is 
# a post code from Belgium or not
def process_address_tag(k_value_list, v_value):
    tag_key = None
    tag_value = None
    
    if k_value_list[1] == 'city':
        tag_key = 'address'
        tag_value = {}
        tag_value[k_value_list[1]] = clean_city_name(v_value)
    elif k_value_list[1] == 'postcode':
        tag_key, tag_value = process_postcode_tag(v_value)
    else:
        tag_key = 'address'
        tag_value = {}
        tag_value[k_value_list[1]] = v_value
        
    return tag_key, tag_value

# given a postcode, identify it is a postcode from the Netherlands or not.
def process_postcode_tag(postcode):
    tag_key = None
    tag_value = None
    
    if re.match(nl_postcode, postcode):
        tag_key = 'NL'
        tag_value = None
    else:
        tag_key = 'address'
        tag_value = {}
        tag_value['postcode'] = postcode
        
    return tag_key, tag_value
    
    
# Clean the phone numbers according to following rules.
# 1. If phone number starts with '+32', set it to '032'
# 2. If phone number contains brackets, remove the numbers in brackets
#       E.g. +32 (0)3 887 46 12 -> 03238874612
# 3. If phone number contains space, remove all spaces
def clean_phone_number(phone):
    phone = phone.replace(" ", "")
    if phone.startswith('+'):
        phone = string.replace(phone, '+', '0', 1)
    phone = re.sub(brackets, '', phone)
    return phone

# Clean the city name according to following rules.
# 1. Capital letters change to small letters, e.g. Berchem -> berchem
# 2. Change city names that are in Dutch to English: antwerpen -> antwerp
# 3. City names with remarks that this city is part of the Antwerp distrct: 
#    'Berchem (Antwerpen)', remove the content in brackets, e.g.
#    Berchem (Antwerpen) -> berchem
# 4. Similar with 3, but with hyphen: 'Hoboken-Antwerpen' -> hoboken
# 5. Similar with 3, but with comma: 'Borgerhout, Antwerp' -> borgerhout
# 6. Remove special characters within city names: '<verschillend>' -> verschillend

def clean_city_name(city):
    city = city.lower()

    if 'antwerpen' in city:
        city = city.replace('antwerpen', 'antwerp')
    if re.search(antwerp, city):
        city = re.sub(antwerp, '', city)
    if '<' in city:
        city = city.replace('<', '')
    if '>' in city:
        city = city.replace('>', '')
        
    return city



def main():
    process_map(FILE_OSM, False)


if __name__ == "__main__":
    main()
    
    
    
    