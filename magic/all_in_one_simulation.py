import argparse
import pathlib
import pandas as pd
import os
import sys
import h5py
import yaml
import numpy as np
import random
import time
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics


def get_data_from_nice_trips(data, nice_trips, count):
    frames = []
    for id in data['class'].unique():
        # id = str(id)
        for i in range(count):
            r = randint(0, len(nice_trips[id]) - 1)
            if len(nice_trips[id][r]) == 0:
                break

            trip = nice_trips[id][r]
            del nice_trips[id][r]
            tdata = data[data['class'] == id]
            frames.append(tdata.loc[trip['start']:trip['end']])

    return pd.concat(frames, sort=False), nice_trips


def main():

    my_parser = argparse.ArgumentParser(
        description='All in one simulation')
    my_parser.add_argument('-p',
                           '--profiles',
                           action='store',
                           metavar='profiles',
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

    my_parser.add_argument('-t',
                           '--trips',
                           action='store',
                           metavar='trips',
                           type=str,
                           required=True,
                           help='Config file with trips')

    # Execute the parse_args() method
    args = my_parser.parse_args()

    profiles = args.profiles
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
    if not os.path.isdir(profiles):
        print('The hdf5 input path specified is not a directory')
        sys.exit()

    for file in os.listdir(profiles):
        if not file.endswith('.hdf'):
            continue

        data = pd.read_hdf(os.path.join(profiles, file))
        frames.append(data)

    data = pd.concat(frames, sort=False)

    features = config['features'][:config['feature_count']]

    data['class'] = data['class'].astype(int)
    train_data, nice_trips = get_data_from_nice_trips(data, nice_trips, 20)
    X_train = train_data[features]
    X_train = X_train.values
    y_train = train_data['class']
    y_train = y_train.squeeze()
    y_train = y_train.astype(int)

    clf = RandomForestClassifier(n_estimators=config['n_estimators'],
                                 n_jobs=-1,
                                 random_state=1,
                                 min_samples_leaf=config['min_samples_leaf'],
                                 criterion=config['criterion'],
                                 max_depth=None)
    clf.fit(X_train, y_train)
    print('Trained model')

    duration = np.timedelta64(60, 's')
    id_to_sim = 0
    sim_data = data[data['class'] == id_to_sim]
    while len(nice_trips[id_to_sim]) > 0:
        trip, nice_trips = get_data_from_nice_trips(sim_data, nice_trips, 1)
        pred_frames = []
        for i in range(int(len(trip) / 30)):
            start = trip.index[i * 30]
            tmp = sim_data[start:start + duration]
            pred_frames.append(tmp)
            pred_data = pd.concat(pred_frames, sort=False)
            X = pred_data[features].values
            pred = clf.predict(X)

            print('Result:\n')
            count = 0
            unique, counts = np.unique(pred, return_counts=True)
            t = dict(zip(unique, counts))
            print(t)
            for id in t:
                c = t[id]
                print('%d: %f' % (id, c / len(pred)))
                if c > count:
                    count = c
                    estimated_driver = id

            conf = count / len(pred)
            if conf > 0.75:
                print('\nDriver is %s with confidence %f' %
                    (estimated_driver, conf))
            time.sleep(2)
        print('End of trip')


main()