#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
In this problem set you work with cities infobox data, audit it, come up with a
cleaning idea and then clean it up. In the first exercise we want you to audit
the datatypes that can be found in some particular fields in the dataset.
The possible types of values can be:
- NoneType if the value is a string "NULL" or an empty string ""
- list, if the value starts with "{"
- int, if the value can be cast to int
- float, if the value can be cast to float, but CANNOT be cast to int.
   For example, '3.23e+07' should be considered a float because it can be cast
   as float but int('3.23e+07') will throw a ValueError
- 'str', for all other values

The audit_file function should return a dictionary containing fieldnames and a 
SET of the types that can be found in the field. e.g.
{"field1": set([type(float()), type(int()), type(str())]),
 "field2": set([type(str())]),
  ....
}
The type() function returns a type object describing the argument given to the 
function. You can also use examples of objects to create type objects, e.g.
type(1.1) for a float: see the test function below for examples.

Note that the first three rows (after the header row) in the cities.csv file
are not actual data points. The contents of these rows should note be included
when processing data types. Be sure to include functionality in your code to
skip over or detect these rows.
"""

import csv
import pprint
import re

CITIES = 'cities.csv'

FIELDS = ["name", "timeZone_label", "utcOffset", "homepage", "governmentType_label",
          "isPartOf_label", "areaCode", "populationTotal", "elevation",
          "maximumElevation", "minimumElevation", "populationDensity",
          "wgs84_pos#lat", "wgs84_pos#long", "areaLand", "areaMetro", "areaUrban"]

def audit_file(filename, fields):
    fieldtypes = {}

    # YOUR CODE HERE
    with open(filename, 'r') as csvfile:
        cities_reader = csv.reader(csvfile, delimiter = ',')
        headers = cities_reader.next()
        
        # create an empty set for each of the header name
        temp_field_types = []
        for header in headers:
            temp_field_types.append(set())
        
        # skip the first 3 lines
        for i in range(3):
            cities_reader.next()
            
        # start reading data
        for line in cities_reader:
            line = [validate_string(cell) for cell in line]
            for i in range(len(line)):
                temp_field_types[i].add(type(line[i]))

    csvfile.close()            
    
    fieldtypes = dict(zip(headers, temp_field_types))
            
    return fieldtypes


def validate_string(cell):
    
    if cell == "NULL" or cell == "":
        return None

    elif cell.startswith('{'):
        cell = re.sub("[{}]", "", cell).split('|')
        for element in cell:
            if is_int(element):
                element = int(element)
            elif is_float(element):
                element = float(element)
        return cell

    elif is_int(cell):
        return int(cell)

    elif is_float(cell):
        return float(cell)

    else:
        return cell


def is_int(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def is_float(s):
    try: 
        float(s)
        return True
    except ValueError:
        return False

def test():
    fieldtypes = audit_file(CITIES, FIELDS)

    pprint.pprint(fieldtypes)

    assert fieldtypes["areaLand"] == set([type(1.1), type([]), type(None)])
    assert fieldtypes['areaMetro'] == set([type(1.1), type(None)])
    
if __name__ == "__main__":
    test()
