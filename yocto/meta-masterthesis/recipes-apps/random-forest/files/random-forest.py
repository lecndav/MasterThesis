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
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics


def main():

    my_parser = argparse.ArgumentParser(
        description='Random forest classifier for driver identification')
    my_parser.add_argument('-c',
                           '--config',
                           action='store',
                           metavar='config',
                           type=str,
                           required=True,
                           help='Config file for rf parameter')

    my_parser.add_argument('-s',
                           '--simulation',
                           action='store',
                           metavar='simulation',
                           type=bool,
                           default=False,
                           help='Enables simulation mode')

    args = my_parser.parse_args()
    config_file = args.config
    simulation = args.simulaiton

    print('Starting random-forest.py')

    config = dict()
    with open(config_file, 'r') as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    if not os.path.isdir(config['input_dir']):
        print('Input directory does not exist')
        exit(1)

    if not os.path.isdir(config['profile_dir']):
        print('Directory with profiles does not exist')
        exit(1)

    if not os.path.isdir(config['sim_profile_dir']):
        print('Directory with simulation profiles does not exist')
        exit(1)

    # read driver profiles
    prfile_dir = config['profile_dir']
    if simulation:
        prfile_dir = config['sim_profile_dir']

    frames = []
    for file in os.listdir(profiles_dir):
        if not file.endswith('.hdf'):
            continue

        data = pd.read_hdf(os.path.join(prfile_dir, file))
        frames.append(data)

    print('Loaded driver profiles')
    profiles = pd.concat(frames, sort=False)
    features = profiles.columns
    features.remove('class')
    X = profiles[features]
    Y = profiles['class']

    X = X.values
    X = np.nan_to_num(X)
    Y = Y.squeeze()
    Y = Y.astype(int)

    # Train RF Classifier
    clf = RandomForestClassifier(n_estimators=config['n_estimators'],
                                 n_jobs=-1,
                                 random_state=1,
                                 min_samples_leaf=config['min_samples_leaf'],
                                 criterion=config['criterion'],
                                 max_depth=config['max_depth'])
    clf.fit(X, Y)
    print('Created and trained ML Model')

    all_data = []
    while True:
        data = []
        for file in os.listdir(config['input_dir']):
            if not file.endswith('.hdf'):
                continue

            df = pd.read_hdf(os.path.join(config['input_dir'], file))
            data.append(df)

            # move file to backup
            os.rename(os.path.join(config['input_dir'], file),
                      os.path.join(config['backup_dir'], file))

        if len(data) == 0:
            continue

        print('New data available...')
        all_data.append(data)
        pdata = all_data[features].values

        print('Predicting...')
        pred = clf.predict(pdata)

        print('Result:\n')
        count = 0
        for id in pred.unique():
            c = pred.count(id)
            print('%d: %f' % (id, c / len(pred)))
            if c > count:
                count = c
                estimated_driver = id

        conf = count / len(pred)
        if conf > config['threshold']:
            print('\nDriver is %s with confidence %f' % (estimated_driver, conf))

        time.sleep(5)


main()