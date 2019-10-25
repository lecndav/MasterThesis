import argparse
import pathlib
import pandas as pd
import os
import sys
import h5py
import numpy as np
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics


def main():

  my_parser = argparse.ArgumentParser(description='Optimize magic.')
  my_parser.add_argument('-i', '--input',
                         action='store',
                         metavar='hdf5_input',
                         type=str,
                         required=True,
                         help='Input directory with source hdf5 files')

  # Execute the parse_args() method
  args = my_parser.parse_args()

  hdf5_input = args.input

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


  X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.1)

  clf = RandomForestClassifier(n_estimators=1000, n_jobs=-1, random_state=1, min_samples_leaf=1)

  n_estimators = [500, 800, 1000, 1200, 1400, 1600, 1800, 2000]
  max_depth = [10, 15, 25, 30, 40, 50, 60]
  min_samples_leaf = [1, 2, 5, 10] 
  criterion = ['gini', 'entropy']

  hyperF = dict(
    n_estimators = n_estimators,
    max_depth = max_depth, 
    min_samples_leaf = min_samples_leaf,
    criterion = criterion
    )

  gridF = GridSearchCV(clf, hyperF, cv = 3, verbose = 1, n_jobs = -1)
  bestF = gridF.fit(X_train, y_train)

  y_pred = bestF.predict(X_test)
  print(bestF.score(X_train, y_train))
  print(gridF.best_params_)
  print("Accuracy:" , metrics.accuracy_score(y_test, y_pred))


main()
