import argparse
import pathlib
import pandas as pd
import os
import sys
import h5py
import yaml
import numpy as np
import random
# from tsfresh import extract_features, select_features, extract_relevant_features
from tsfresh.feature_extraction import extract_features
from tsfresh.feature_extraction.settings import TimeBasedFCParameters
from tsfresh.utilities.dataframe_functions import impute
import matplotlib.pyplot as plt
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'lib'))
from helper import get_trips_from_hdf, get_data_from_random_trips


def main():

    my_parser = argparse.ArgumentParser(
        description='Magic random forest classifier')
    my_parser.add_argument('-i',
                           '--input',
                           action='store',
                           metavar='hdf5_input',
                           type=str,
                           required=True,
                           help='Input directory with source hdf5 files')

    my_parser.add_argument('-c',
                           '--config',
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
        # data.reset_index(level=0, inplace=True)
        frames.append(data)

    data = pd.concat(frames, sort=False)

    trips = get_trips_from_hdf(data)
    time = 15 * 30

    tdata = get_data_from_random_trips(trips, data, time)
    features = config['features'][:config['feature_count']]
    tdata = tdata[features + ['class']]
    X = tdata[features]
    Y = tdata['class']
    # X = np.nan_to_num(X)
    settings_time = TimeBasedFCParameters()
    X_filtered = extract_features(tdata,
                                  Y,
                                  column_id='class',
                                  default_fc_parameters=settings_time)
    X_filtered.head()
    X_filtered.info()

    X_train, X_test, y_train, y_test = train_test_split(X_filtered,
                                                        Y,
                                                        test_size=0.3)

    clf = RandomForestClassifier(n_estimators=config['n_estimators'],
                                 n_jobs=-1,
                                 random_state=1,
                                 min_samples_leaf=config['min_samples_leaf'],
                                 criterion=config['criterion'],
                                 max_depth=None)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)

    acc = metrics.accuracy_score(y_test, y_pred)
    print(acc)


main()
