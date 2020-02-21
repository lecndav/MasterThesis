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

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'lib'))
from helper import get_trips_from_hdf, get_data_from_random_trips


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

    my_parser.add_argument('-f', '--feature-importance',
                           action='store',
                           metavar='feature_importance',
                           type=str,
                           required=True,
                           help='Dir with feature importance results')

    my_parser.add_argument('-r', '--results-dir',
                           action='store',
                           metavar='results_dir',
                           type=str,
                           required=True,
                           help='Directory for results file')

    # Execute the parse_args() method
    args = my_parser.parse_args()
    config_file = args.config
    hdf5_input = args.input
    results_dir = args.results_dir
    feature_importance = args.feature_importance

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

    csv_res = pd.DataFrame()
    for file in os.listdir(feature_importance):
        if not file.endswith('.csv'):
            continue
        t = pd.read_csv(os.path.join(feature_importance, file))
        csv_res = csv_res.append(t, sort=True)

    signals = (list(set(csv_res.columns) - set(['accuracy'])))
    csv_res = csv_res[signals].mean(axis=0).sort_values(
        ascending=False).to_frame()

    f_list = csv_res.T.columns

    csv_columns = ['accuracy', 'feature_count']
    trips = get_trips_from_hdf(data)
    time = 20 * 30

    for x in range(100):
        c = len(os.listdir(results_dir))
        csv_file = os.path.join(results_dir, 'feature_selection_%d.csv' % c)
        csvfile = open(csv_file, 'w')
        writer = csv.DictWriter(csvfile, csv_columns)
        writer.writeheader()

        tdata = get_data_from_random_trips(trips, data, time)
        print(tdata.head())

        for i in range(len(f_list) - 1, 0, -1):
            X = tdata[f_list[0:i]]
            Y = tdata['class']
            X = np.nan_to_num(X)
            X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3)

            clf = RandomForestClassifier(n_estimators=config['n_estimators'], n_jobs=-1, random_state=1,
                                        min_samples_leaf=config['min_samples_leaf'], criterion=config['criterion'], max_depth=None)
            clf.fit(X_train, y_train)
            y_pred = clf.predict(X_test)
            accuracy = metrics.accuracy_score(y_test, y_pred)
            print('accuracy: %f, count: %d' % (accuracy, i))
            writer.writerow({'accuracy': accuracy, 'feature_count': i})

        csvfile.close()


main()
