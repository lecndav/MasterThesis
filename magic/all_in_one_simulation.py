import argparse
import pathlib
import pandas as pd
import os
import sys
import yaml
import numpy as np
import time
from random import randint
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics


def send_SMS(message, number):
    print(message)


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

    print('Started')
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

    my_parser.add_argument('-s',
                           '--thief',
                           action='store',
                           metavar='thief',
                           type=str,
                           required=True,
                           help='Testdata of a thief')

    # Execute the parse_args() method
    args = my_parser.parse_args()

    profiles = args.profiles
    config_file = args.config
    trips_file = args.trips
    thief_file = args.thief

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
    print('Loaded profiles')

    features = config['features'][:config['feature_count']]

    data['class'] = data['class'].astype(int)
    train_data, nice_trips = get_data_from_nice_trips(data, nice_trips, 10)
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

    if not thief_file:
        id_to_sim = 3
        sim_data = data[data['class'] == id_to_sim]
    else:
        sim_data = pd.read_hdf(thief_file)
        sim_data['class'] = sim_data['class'].astype(int)
        id_to_sim = sim_data['class'][0]

    while len(nice_trips[id_to_sim]) > 0:
        trip, nice_trips = get_data_from_nice_trips(sim_data, nice_trips, 1)
        pred_frames = []
        confirmed_id = None
        confirmation_count = 0
        thief_count = 0
        for i in range(int(len(trip) / 30)):
            start = trip.index[i * 30]
            tmp = sim_data[start:start + duration]
            pred_frames.append(tmp)
            pred_data = pd.concat(pred_frames, sort=False)
            X = pred_data[features].values
            pred = clf.predict(X)

            print('Result:\n')
            unique, counts = np.unique(pred, return_counts=True)
            t = dict(zip(unique, counts))
            print(t)
            first = {'id': None, 'count': 0}
            second = {'id': None, 'count': 0}
            for id in t:
                c = t[id]
                if c > first['count']:
                    first['count'] = c
                    first['id'] = id
                elif c > second['count']:
                    second['count'] = c
                    second['id'] = id

            first_conf = first['count'] / len(pred)
            second_conf = second['count'] / len(pred)
            diff = first_conf - second_conf
            if diff >= 0.30 and first_conf >= 0.50:
                thief_count = 0
                if confirmed_id == first['id']:
                    confirmation_count += 1
                else:
                    confirmed_id = first['id']
                    confirmation_count = 1
            else:
                thief_count += 1
            if confirmation_count == config['confirmation_count']:
                send_SMS('\nDriver with id %s is driving' % first['id'],
                         config['number'])
                break

            if thief_count == config['thief_count']:
                send_SMS('\nA potential thief is driving', config['number'])
                break
            time.sleep(1)
        print('End of trip')


main()