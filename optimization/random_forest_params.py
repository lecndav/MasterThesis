import argparse
import pathlib
import pandas as pd
import os
import sys
import h5py
import numpy as np
import csv
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics

n_estimators = [300, 400, 500, 600, 650, 700, 800,
                1000, 1200, 1300, 1350, 1400, 1500, 1600, 1800, 2000]
max_depth = [5, 7, 9, 10, 12, 13, 15, 17, 18]
min_samples_leaf = [1, 3, 4, 5, 6]
criterion = ['gini', 'entropy']
# duration = [5, 8, 10, 12, 14, 16, 18, 20, 25, 30, 35]
# window_size = [900, 1000, 1500, 1800, 2000, 2200, 2500, 2800, 3000]


def main():

  my_parser = argparse.ArgumentParser(description='Optimize magic.')
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


  # Execute the parse_args() method
  args = my_parser.parse_args()

  hdf5_input = args.input
  results_dir = args.results_dir

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


  X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3)

  clf = RandomForestClassifier(n_jobs=-1, random_state=0)

  hyperF = dict(
    n_estimators = n_estimators,
    max_depth = max_depth,
    min_samples_leaf = min_samples_leaf,
    criterion = criterion
    )

  gridF = GridSearchCV(clf, hyperF, cv=3, verbose=1, n_jobs=-1, return_train_score=True)
  gridF.fit(X_train, y_train)

  csv_columns = list(gridF.best_params_.keys()) + ['time', 'accuracy']
  c = len(os.listdir(results_dir))
  csv_file = os.path.join(results_dir, 'random_forest_params_%d.csv' % c)
  means = gridF.cv_results_['mean_test_score']
  time = gridF.cv_results_['mean_fit_time']

  with open(csv_file, 'w') as csvfile:
    writer = csv.DictWriter(csvfile, csv_columns)
    writer.writeheader()
    for mean, t, params in zip(means, time, gridF.cv_results_['params']):
      params.update({'time': t, 'accuracy': mean})
      writer.writerow(params)


main()
