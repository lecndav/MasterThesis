import argparse
import pathlib
import pandas as pd
import os
import sys
import h5py
import yaml
import numpy as np
import random
import rfpimp
import matplotlib.pyplot as plt
from collections import defaultdict
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
# from sklearn.inspection import permutation_importance
from sklearn import metrics
from scipy.stats import spearmanr
from scipy.cluster import hierarchy
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'lib'))
from helper import get_trips_from_hdf, get_data_from_random_trips


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

  trips = get_trips_from_hdf(data)
  time = 15 * 30

  tdata = get_data_from_random_trips(trips, data, time)
  features = config['features'][:config['feature_count']]
  X = tdata[features]
  Y = tdata['class']
  X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3)

  clf = RandomForestClassifier(n_estimators=config['n_estimators'], n_jobs=-1, random_state=1, min_samples_leaf=config['min_samples_leaf'], criterion=config['criterion'], max_depth=None)
  clf.fit(X_train, y_train)
  y_pred = clf.predict(X_test)

  acc = metrics.accuracy_score(y_test, y_pred)
  print(acc)

  imp = rfpimp.importances(clf, X_train, y_train.to_frame())
  print(imp)


main()
