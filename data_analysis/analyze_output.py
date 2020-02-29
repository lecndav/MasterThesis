import argparse
import pathlib
import pandas as pd
import os
import sys
import h5py
import yaml
import numpy as np
import random
import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter
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
        frames.append(data)

    data = pd.concat(frames, sort=False)

    trips = get_trips_from_hdf(data)
    time = 30 * 30

    tdata = get_data_from_random_trips(trips, data, time)
    # tdata = tdata[tdata['can0_ESP_Bremsdruck_median'] < 0.5]
    features = config['features'][:config['feature_count']]
    X = tdata[features]
    Y = tdata['class']
    X = np.nan_to_num(X)
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3)

    clf = RandomForestClassifier(n_estimators=config['n_estimators'],
                                 n_jobs=-1,
                                 random_state=1,
                                 min_samples_leaf=config['min_samples_leaf'],
                                 criterion=config['criterion'],
                                 max_depth=None)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    i = 0
    x1 = 0
    x2 = 0
    false_x = pd.DataFrame(columns=features)
    true_x = pd.DataFrame(columns=features)
    false_y = []
    for c in y_pred:
        if c != y_test[i]:
            false_x.loc[x1] = X_test[i]
            false_y.append(y_test[i])
            x1 += 1
        else:
            true_x.loc[x2] = X_test[i]
            x2 += 1
        i += 1



    acc = metrics.accuracy_score(y_test, y_pred)
    print(acc)

    # plot signal for true and false datapoints
    if False:
        fig1 = plt.figure()
        plt.title('False')
        plt.scatter(x=range(len(false_x)),
                    y=false_x['can0_ESP_Bremsdruck_median'],
                    s=2)
        fig2 = plt.figure()
        plt.title('True')
        plt.scatter(x=range(len(true_x)),
                    y=true_x['can0_ESP_Bremsdruck_median'],
                    s=2)
    #

    # plot distribution
    if True:
        figdist = plt.figure()
        sns.distplot(false_x['can0_ESP_Bremsdruck_mean'], color='blue', hist=False, kde=True)
        sns.distplot(true_x['can0_ESP_Bremsdruck_mean'], color='orange', hist=False, kde=True)
    #

    # plt.show()



main()
