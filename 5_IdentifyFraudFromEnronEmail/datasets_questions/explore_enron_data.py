#!/usr/bin/python

""" 
    Starter code for exploring the Enron dataset (emails + finances);
    loads up the dataset (pickled dict of dicts).

    The dataset has the form:
    enron_data["LASTNAME FIRSTNAME MIDDLEINITIAL"] = { features_dict }

    {features_dict} is a dictionary of features associated with that person.
    You should explore features_dict as part of the mini-project,
    but here's an example to get you started:

    enron_data["SKILLING JEFFREY K"]["bonus"] = 5600000
    
"""

import pickle

enron_data = pickle.load(open("../final_project/final_project_dataset.pkl", "r"))

total_person = 0
num_poi = 0
salary_count = 0
email_count = 0
total_payment_count = 0
total_payment_poi = 0

person_names = [x for x in enron_data.keys()]
person_attrs = enron_data['LAY KENNETH L'].keys()

for person, feature_dict in enron_data.items():
    total_person += 1
    if feature_dict['poi'] == 1:
        num_poi += 1
    if feature_dict['salary'] != 'NaN':
        salary_count += 1
    if feature_dict['email_address'] != 'NaN':
        email_count += 1
    if feature_dict['total_payments'] == 'NaN':
        total_payment_count += 1
        if feature_dict['poi'] == 1:
            total_payment_poi += 1

print "Total number of people: ", total_person
print "Total number of POIs is: ", num_poi
print "Number of people having a salary value is: ", salary_count
print "Number of people having an email value is: ", email_count
print "Number of people having NaN total payment is: ", total_payment_count
print "Number of POI having NaN total payment is: ", total_payment_poi

print "The exercised stock options of Jeffrey Skilling is: ", enron_data['SKILLING JEFFREY K']['exercised_stock_options']
# print enron_data['LAY KENNETH L']
# print enron_data['FASTOW ANDREW S']


import sys
sys.path.append( "../tools/" )
from feature_format import featureFormat, targetFeatureSplit

feature_list = ['poi', 'salary', 'to_messages', 'deferral_payments', 'total_payments', 'exercised_stock_options',
                'bonus', 'restricted_stock', 'shared_receipt_with_poi', 'restricted_stock_deferred',
                'total_stock_value', 'expenses', 'loan_advances', 'from_messages', 'other', 'from_this_person_to_poi',
                'director_fees', 'deferred_income', 'long_term_incentive', 'from_poi_to_this_person']

data_array = featureFormat(enron_data, feature_list)
label, features = targetFeatureSplit(data_array)