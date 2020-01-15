import argparse
import pathlib
import pandas as pd
import os
import sys
import h5py
import numpy as np
import csv
import random
import yaml
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics

duration = [5, 8, 10, 13, 16, 18, 20, 25, 30, 35]

def main():

  my_parser = argparse.ArgumentParser(description='Train duration check')
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

  my_parser.add_argument('-c', '--config',
                         action='store',
                         metavar='config',
                         type=str,
                         required=True,
                         help='Config file for rf parameter')

  # Execute the parse_args() method
  args = my_parser.parse_args()

  hdf5_input = args.input
  results_dir = args.results_dir
  config_file = args.config

  config = dict()
  with open(config_file, 'r') as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)


  frames = []
  if not os.path.isdir(hdf5_input):
    print('The hdf5 input path specified is not a directory')
    sys.exit()

  for file in os.listdir(hdf5_input):
    if not file.endswith('.hdf'):
      continue

    data = pd.read_hdf(os.path.join(hdf5_input, file))
    frames.append(data)

  csv_columns = ['duration', 'accuracy']
  csv_file = os.path.join(results_dir, 'duration_everytime_new.csv')
  csvfile = open(csv_file, 'w')
  writer = csv.DictWriter(csvfile, csv_columns)
  writer.writeheader()

  for i in range(0, 50):
    for d in duration:
      count = d * 30 * 1.3
      count = int(count)
      tempa = []
      for frame in frames:
        s = random.randint(0, len(frame) - count)
        frame.reset_index(drop=True, inplace=True)
        tempa.append(frame[s:s+count])

      temp = pd.concat(tempa, sort=False)
      temp = shuffle(temp)
      columns = list(temp.head())
      columns.remove('class')
      X = temp[columns]
      Y = temp['class']
      X = np.nan_to_num(X)

      X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3)

      clf = RandomForestClassifier(n_estimators=config['n_estimators'], n_jobs=-1, random_state=1)
      clf.fit(X_train, y_train)
      y_pred = clf.predict(X_test)

      accuracy = metrics.accuracy_score(y_test, y_pred)
      print('d: %d a: %f' % (d, accuracy))
      writer.writerow({'duration': d, 'accuracy': accuracy})



main()
