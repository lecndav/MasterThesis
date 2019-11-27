import argparse
import pathlib
import pandas as pd
import os
import sys
import numpy as np
import csv
import yaml
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics


def main():

  my_parser = argparse.ArgumentParser(description='Analyse feature importance')
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
  config_file = args.config
  hdf5_input = args.input

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

  result = pd.concat(frames, sort=False)
  result = shuffle(result)
  columns = list(result.head())
  columns.remove('class')

  features = config['features']
  X = result[columns]
  Y = result['class']
  X = np.nan_to_num(X)
  X_train, X_test, y_train, y_test = train_test_split(
      X, Y, test_size=config['test_size'])

  clf = RandomForestClassifier(n_estimators=config['n_estimators'], n_jobs=-1, random_state=1,
                               min_samples_leaf=config['min_samples_leaf'], criterion=config['criterion'], max_depth=config['max_depth'])
  clf.fit(X_train, y_train)
  y_pred = clf.predict(X_test)

main()
