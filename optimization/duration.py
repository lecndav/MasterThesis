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

duration = [5, 8, 10, 12, 14, 16, 18, 20, 25, 30, 35]
# window_size = [900, 1000, 1500, 1800, 2000, 2200, 2500, 2800, 3000]

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

  my_parser.add_argument('-s', '--window-size',
                         action='store',
                         metavar='windowsize',
                         type=str,
                         required=True,
                         help='Window size in ms')

  # Execute the parse_args() method
  args = my_parser.parse_args()

  hdf5_input = args.input
  results_dir = args.results_dir
  window_size = args.window_size

  frames = []
  if not os.path.isdir(hdf5_input):
    print('The hdf5 input path specified is not a directory')
    sys.exit()

  results = dict()
  for d in duration:
    i = 0
    for file in os.listdir(hdf5_input):
      if not file.endswith('.hdf'):
        continue
      if i == d:
        break
      i += 1

      data = pd.read_hdf(os.path.join(hdf5_input, file))
      data = data.iloc[:((d * 60) / (window_size / 1000))]
      frames.append(data)

    result = pd.concat(frames, sort=False)
    result = shuffle(result)
    columns = list(result.head())
    columns.remove('class')
    X = result[columns]
    Y = result['class']
    X = np.nan_to_num(X)
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3)

    clf = RandomForestClassifier(n_estimators=1000, n_jobs=-1, random_state=1, min_samples_leaf=1, criterion='entropy')
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)

    accuracy = metrics.accuracy_score(y_test, y_pred)
    results[d] = accuracy

  csv_columns = ['duration', 'accuracy']
  csv_file = os.path.join(results_dir, 'duration.csv')
  with open(csv_file, 'w') as csvfile:
    writer = csv.DictWriter(csvfile, csv_columns)
    writer.writeheader()
    writer.writerows(results)


main()
