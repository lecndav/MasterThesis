import argparse
import pathlib
import pandas as pd
import os
import sys
import h5py
import csv
import numpy as np
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics


def main():

  my_parser = argparse.ArgumentParser(description='Magic random forest classifier')
  my_parser.add_argument('-i', '--input',
                         action='store',
                         metavar='hdf5_input',
                         type=str,
                         required=True,
                         help='Input directory with source hdf5 files')

  my_parser.add_argument('-r', '--results-dir',
                         action='store',
                         metavar='results_dir',
                         type=str,
                         required=True,
                         help='Directory for results file')

  my_parser.add_argument('-e', '--estimators',
                         action='store',
                         metavar='estimators',
                         type=int,
                         required=False,
                         default=1000,
                         help='n_estimator for Random Forest Classifier')

  my_parser.add_argument('-d', '--max-depth',
                         action='store',
                         metavar='max_depth',
                         type=int,
                         required=False,
                         default=15,
                         help='max_depth for Random Forest Classifier')

  # Execute the parse_args() method
  args = my_parser.parse_args()

  hdf5_input = args.input
  results_dir = args.results_dir
  n_estimators = args.estimators
  max_depth = args.max_depth

  frames = []
  if not os.path.isdir(hdf5_input):
    print('The hdf5 input path specified is not a directory')
    sys.exit()

  for file in os.listdir(hdf5_input):
    if not file.endswith('.hdf'):
      continue

    data = pd.read_hdf(os.path.join(hdf5_input, file))
    frames.append(data)

  result = pd.concat(frames, sort=False)
  result = shuffle(result)
  columns = list(result.head())
  columns.remove('class')
  X = result[columns]
  Y = result['class']
  X = np.nan_to_num(X)

  csv_columns = ['n_estimators', 'max_depth', 'accuracy']
  c = len(os.listdir(results_dir))
  csv_file = os.path.join(results_dir, 'random_forest_params_detailed_%d.csv' % c)
  csvfile = open(csv_file, 'w')
  writer = csv.DictWriter(csvfile, csv_columns)
  writer.writeheader()

  for i in range(0,100):
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2)
    clf = RandomForestClassifier(n_estimators=n_estimators, n_jobs=-1, criterion='gini', max_depth=max_depth)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)

    accuracy = metrics.accuracy_score(y_test, y_pred)
    writer.writerow({'n_estimators': n_estimators, 'max_depth': max_depth, 'accuracy': accuracy})

  csvfile.close()


main()
