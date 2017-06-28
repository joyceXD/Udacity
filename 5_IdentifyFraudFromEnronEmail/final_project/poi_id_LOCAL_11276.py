#!/usr/bin/python

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pickle
import sys

sys.path.append("../tools/")

from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data

# Functions to be used in this project
def calc_ratio(value, total):
    if total == 0:
        return 0
    else:
        return float(float(value) / float(total))

# Task 1: Select what features you'll use.
# features_list is a list of strings, each of which is a feature name.
# The first feature must be "poi".
features_list = ['poi', 'salary', 'to_messages', 'deferral_payments', 'total_payments',
                 'exercised_stock_options', 'bonus', 'restricted_stock', 'shared_receipt_with_poi',
                 'restricted_stock_deferred', 'total_stock_value', 'expenses', 'loan_advances',
                 'from_messages', 'other', 'from_this_person_to_poi', 'director_fees', 'deferred_income',
                 'long_term_incentive', 'from_poi_to_this_person']  # 'email_address' is excluded

# Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)

# Store to my_dataset for easy export below.
my_dataset = data_dict
print len(data_dict.keys())

# Extract features and labels from dataset for local testing
data = featureFormat(dictionary = my_dataset,
                     features = features_list,
                     remove_NaN = True,
                     remove_all_zeroes = True,
                     remove_any_zeroes = False,
                     sort_keys=False)

labels, features = targetFeatureSplit(data)


# Convert to pandas dataframe
features = pd.DataFrame(features)

# for i in range(1, len(features.columns)):
#     # fig = plt.figure()
#     # ax = fig.add_subplot(111)
#     # ax.boxplot(features.iloc[:, i - 1])
#     plt.hist(features.iloc[:, i - 1], 100, facecolor='green', alpha=0.75)
#     plt.xlabel(features_list[i])
#     plt.savefig('./plot/hist_{}.png'.format(features_list[i]))

# Task 2: Remove outliers

features.columns = features_list[1:]
print features.columns.values

# Task 3: Create new feature(s)
features['from_this_person_to_poi_fraction'] = features.apply(lambda row: calc_ratio(row['from_this_person_to_poi'],
                                                                                     row['from_messages']),
                                                              axis=1)
features['from_poi_to_this_person_fraction'] = features.apply(lambda row: calc_ratio(row['from_poi_to_this_person'],
                                                                                     row['to_messages']),
                                                              axis=1)
features['bonus_over_payment_ratio'] = features.apply(lambda row: calc_ratio(row['bonus'],
                                                                              row['total_payments']),
                                                       axis=1)
features['exercised_stock_ratio'] = features.apply(lambda row: calc_ratio(row['exercised_stock_options'],
                                                                          row['total_stock_value']),
                                                   axis=1)

# Explore and visualize statistics of each column to find outliers
print features.describe()

# Task 4: Try a variaty of classifiers
# Please name your classifier clf for easy export below.
# Note that if you want to do PCA or other multi-stage operations,
# you'll need to use Pipelines. For more info:
# http://scikit-learn.org/stable/modules/pipeline.html

# Provided to give you a starting point. Try a variety of classifiers.
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from sklearn.decomposition import PCA
from sklearn.feature_selection import SelectKBest, chi2

pipe = Pipeline([
    ('reduce_dim', PCA()),
    ('classify', LinearSVC())
])

N_FEATURES_OPTIONS = 10
C_OPTIONS = [1, 10, 100, 1000]
param_grid = [
    {
        'reduce_dim': PCA(iterated_power=7),
        'reduce_dim__n_components': N_FEATURES_OPTIONS,
        'classify__C': C_OPTIONS
    },
    {
        'reduce_dim': [SelectKBest(chi2)],
        'reduce_dim__k': N_FEATURES_OPTIONS,
        'classify__C': C_OPTIONS
    },
]
reducer_labels = ['PCA', 'KBest(chi2)']

grid = GridSearchCV(pipe, cv=3, n_jobs=2, param_grid=param_grid)
grid.fit(features, labels)

mean_scores = np.array(grid.cv_results_['mean_test_score'])
# scores are in the order of param_grid iteration, which is alphabetical
mean_scores = mean_scores.reshape(len(C_OPTIONS), -1, len(N_FEATURES_OPTIONS))
# select score for best C
mean_scores = mean_scores.max(axis=0)
bar_offsets = (np.arange(len(N_FEATURES_OPTIONS)) *
               (len(reducer_labels) + 1) + .5)

plt.figure()
COLORS = 'bgrcmyk'
for i, (label, reducer_scores) in enumerate(zip(reducer_labels, mean_scores)):
    plt.bar(bar_offsets + i, reducer_scores, label=label, color=COLORS[i])

plt.title("Comparing feature reduction techniques")
plt.xlabel('Reduced number of features')
plt.xticks(bar_offsets + len(reducer_labels) / 2, N_FEATURES_OPTIONS)
plt.ylabel('Digit classification accuracy')
plt.ylim((0, 1))
plt.legend(loc='upper left')
plt.show()

# Task 5: Tune your classifier to achieve better than .3 precision and recall
# using our testing script. Check the tester.py script in the final project
# folder for details on the evaluation method, especially the test_classifier
# function. Because of the small size of the dataset, the script uses
# stratified shuffle split cross validation. For more info:
# http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html

# Example starting point. Try investigating other evaluation techniques!
from sklearn.cross_validation import train_test_split

features_train, features_test, labels_train, labels_test = \
    train_test_split(features, labels, test_size=0.3, random_state=42)

# Task 6: Dump your classifier, dataset, and features_list so anyone can
# check your results. You do not need to change anything below, but make sure
# that the version of poi_id.py that you submit can be run on its own and
# generates the necessary .pkl files for validating your results.

dump_classifier_and_data(clf, my_dataset, features_list)
