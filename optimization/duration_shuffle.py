import argparse
import pathlib
import pandas as pd
import os
import sys
import h5py
import yaml
import numpy as np
import random
import csv
import matplotlib.pyplot as plt
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'lib'))
from helper import get_trips_from_hdf


def main():

  my_parser = argparse.ArgumentParser(description='Magic random forest classifier')
  my_parser.add_argument('-i', '--input',
                         action='store',
                         metavar='hdf5_input',
                         type=str,
                         required=True,
                         help='Input directory with source hdf5 files')

  my_parser.add_argument('-c', '--config',
                         action='store',
                         metavar='config',
                         type=str,
                         required=True,
                         help='Config file for rf parameter')


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

  data = pd.concat(frames, sort=False)

  trips = get_trips_from_hdf(data)

  csv_columns = ['duration', 'accuracy']
  csv_file = os.path.join(results_dir, 'duration_shuffle.csv')
  csvfile = open(csv_file, 'w')
  writer = csv.DictWriter(csvfile, csv_columns)
  writer.writeheader()


  durations = [5, 7, 8, 10, 12, 14, 16, 18, 20, 22, 25, 30, 35, 40]

  for duration in durations:
    time = duration * 30
    for i in range(0, 50):
      frames = []
      for d in trips:
        tdata = data.loc[data['class'] == d]
        tmp = shuffle(tdata)
        tmp = tmp.iloc[0:time]
        frames.append(tmp)

      tdata = pd.concat(frames, sort=False)
      features = config['features'][:config['feature_count']]
      X = tdata[features]
      Y = tdata['class']
      X = np.nan_to_num(X)
      X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3)

      clf = RandomForestClassifier(n_estimators=config['n_estimators'], n_jobs=-1, random_state=1, min_samples_leaf=config['min_samples_leaf'], criterion=config['criterion'], max_depth=None)
      clf.fit(X_train, y_train)
      y_pred = clf.predict(X_test)

      acc = metrics.accuracy_score(y_test, y_pred)
      writer.writerow({'duration': duration, 'accuracy': acc})

main()
