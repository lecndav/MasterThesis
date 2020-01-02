import argparse
import pathlib
import pandas as pd
import os
import sys
import h5py
import yaml
import numpy as np
from datetime import datetime
from sklearn.utils import shuffle
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'lib'))
from helper import train_test_split_bremsdruck, train_test_split_trip_start


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

  # Execute the parse_args() method
  args = my_parser.parse_args()

  hdf5_input = args.input
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
  data = shuffle(data)

  feature_count = config['feature_count'][:config['feature_count']]
  X = data[features]
  Y = data['class']
  X = np.nan_to_num(X)
  X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3)

  clf = RandomForestClassifier(n_estimators=config['n_estimators'], n_jobs=-1, random_state=1,
                                min_samples_leaf=config['min_samples_leaf'], criterion=config['criterion'], max_depth=None)
  clf.fit(X_train, Y_train)
  Y_pred = clf.predict(X_test)

  accuracy = metrics.accuracy_score(Y_test, Y_pred)
  print('Accuracy', accuracy)


main()
