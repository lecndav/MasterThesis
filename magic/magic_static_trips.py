import argparse
import pathlib
import pandas as pd
import os
import sys
import h5py
import yaml
import numpy as np
import random
import matplotlib.pyplot as plt
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'lib'))
from helper import get_trips_from_hdf, get_data_from_random_trips, get_data_from_nice_trips, get_right_n_wrong_dp


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


  my_parser.add_argument('-t', '--trips',
                         action='store',
                         metavar='trips',
                         type=str,
                         required=True,
                         help='Config file with trips')

  # Execute the parse_args() method
  args = my_parser.parse_args()

  hdf5_input = args.input
  config_file = args.config
  trips_file = args.trips

  config = dict()
  with open(config_file, 'r') as stream:
    try:
      config = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
      print(exc)

  nice_trips = dict()
  with open(trips_file, 'r') as stream:
    try:
      nice_trips = yaml.safe_load(stream)
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

  features = config['features'][:config['feature_count']]

  data['class'] = data['class'].astype(int)
  train_data, nice_trips = get_data_from_nice_trips(data, nice_trips, 5)
  X_train = train_data[features]
  X_train = X_train.values
  y_train = train_data['class']
  y_train = y_train.squeeze()
  y_train = y_train.astype(int)

  clf = RandomForestClassifier(n_estimators=config['n_estimators'], n_jobs=-1, random_state=1, min_samples_leaf=config['min_samples_leaf'], criterion=config['criterion'], max_depth=None)
  clf.fit(X_train, y_train)

  ids = data['class'].unique()
  for id in ids:
    while len(nice_trips[id]) > 0:
      ttrips = {}
      ttrips[id] = nice_trips[id]
      test_data, temp = get_data_from_nice_trips(data, ttrips, 1)
      nice_trips[id] = temp[id]
      if len(test_data) < 1:
        continue
      X_test = test_data[features]
      X_test = X_test.values
      y_test = test_data['class']
      y_test = y_test.squeeze()

      y_pred = clf.predict(X_test)
      acc = metrics.accuracy_score(y_test, y_pred)
      print(id, acc)

    # true_x, false_x = get_right_n_wrong_dp(y_pred, X_test, y_test,
                                            # features)

main()
