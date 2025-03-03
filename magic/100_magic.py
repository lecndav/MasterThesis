import argparse
import pathlib
import pandas as pd
import os
import sys
import h5py
import yaml
import numpy as np
import csv
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

    my_parser.add_argument('-r',
                            '--results-dir',
                            action='store',
                            metavar='results_dir',
                            type=str,
                            required=True,
                            help='Directory for results file')

    # Execute the parse_args() method
    args = my_parser.parse_args()

    hdf5_input = args.input
    config_file = args.config
    results_dir = args.results_dir

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
        data['class'] = int(file.split('_')[0])
        frames.append(data)

    data = pd.concat(frames, sort=False)

    trips = get_trips_from_hdf(data)
    time = 15 * 30

    csv_columns = ['accuracy']
    c = len(os.listdir(results_dir))
    csv_file = os.path.join(results_dir, 'acc_%d.csv' % c)
    csvfile = open(csv_file, 'w')
    writer = csv.DictWriter(csvfile, csv_columns)
    writer.writeheader()

    for i in range(0, 100):
        tdata = get_data_from_random_trips(trips, data, time)
        features = config['features'][:config['feature_count']]
        X = tdata[features]
        Y = tdata['class']
        X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3)

        clf = RandomForestClassifier(
          n_estimators=config['n_estimators'],
          n_jobs=-1,
          random_state=1,
          min_samples_leaf=config['min_samples_leaf'],
          criterion=config['criterion'],
          max_depth=None)
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)

        acc = metrics.accuracy_score(y_test, y_pred)
        print(acc)
        writer.writerow({'accuracy': acc})

    csvfile.close()


main()
