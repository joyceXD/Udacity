# -*- coding: utf-8 -*-
"""
Created on Mon Oct 31 14:36:55 2016

@author: X.Pang
"""

def classify(features_train, labels_train):   
    ### import the sklearn module for GaussianNB
    ### create classifier
    ### fit the classifier on the training features and labels
    ### return the fit classifier
    
    
    ### your code goes here!
    from sklearn.naive_bayes import GaussianNB
    gnb = GaussianNB()
    gnb.fit(features_train, labels_train)
    return gnb
    