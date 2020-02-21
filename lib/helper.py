import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from random import randint, shuffle
from datetime import timedelta, datetime

def order_files(input_path):
    driver = dict()
    for file in os.listdir(input_path):
        if file.split('.')[-1] != 'mf4':
            continue
        id = file.split('_')[1].split('.')[0]
        timestamp = file.split('_')[0]
        if id not in driver:
            driver[id] = []
        driver[id].append(timestamp)

    for id in driver:
        driver[id].sort()

    return driver


def get_trips(driver):
    trips = dict()
    max_trip_delta = 5 * 60 * 1000000000  # 5 minutes
    for d in driver:
        new_trip = True
        trips[d] = []
        tlast = float(driver[d][0])
        for ts in driver[d]:
            t = float(ts)
            if new_trip:
                trips[d].append([])
                new_trip = False
            if (t - tlast) > max_trip_delta:
                tlast = t
                new_trip = True
            else:
                trips[d][-1].append(ts)
                tlast = t
    return trips

def get_trips_from_hdf(data):
    trips = dict()
    ids = data['class'].unique()
    max_trip_delta = np.timedelta64(5 * 60, 's')  # 5 minutes
    for id in ids:
        new_trip = True
        trips[id] = []
        tmp = data.loc[data['class'] == id]
        tmp.sort_index(axis=0, inplace=True)
        ts = list(tmp.index.values)
        tlast = ts[0]
        for t in ts:
            if new_trip:
                trips[id].append([])
                new_trip = False
            if (t - tlast) > max_trip_delta:
                tlast = t
                new_trip = True
            else:
                trips[id][-1].append(t)
                tlast = t
    return trips

def get_data_from_random_trips(trips, data, time):
    frames = []
    for d in trips:
        while True:
            tdata = data.loc[data['class'] == d]

            strip = randint(0, len(trips[d])-5)
            etrip = strip
            ttrip = strip
            tmp_time = time
            diff = time
            while True:
                if len(trips[d][ttrip]) < diff:
                    diff = diff - len(trips[d][ttrip])
                    ttrip += 1
                    continue
                tmp_time = diff
                etrip = ttrip
                break

            try: # trick list index out of bounce
                mask = (tdata.index > trips[d][strip][0]) & (
                    tdata.index <= trips[d][etrip][tmp_time])
            except:
                continue
            tmp = tdata.loc[mask]
            frames.append(tmp)
            break

    return pd.concat(frames, sort=False)


def train_test_split_trip_start(data, test_size):
    train_time = 10 * 60
    test_time = 5 * 60
    columns = data.columns
    features = list(columns)
    features.remove('class')
    X_train = pd.DataFrame(columns=features)
    X_test = pd.DataFrame(columns=features)
    Y_train = pd.DataFrame(columns=['class'])
    Y_test = pd.DataFrame(columns=['class'])
    ids = data['class'].unique()
    trips = get_trips_from_hdf(data)
    for id in ids:
        x = data.loc[data['class'] == id]
        y = x['class'].to_frame()
        x = x[features]

        test_index = randint(0, len(trips[id])-1)
        test_ts = trips[id][test_index]
        del trips[id][test_index]

        shuffle(trips[id])
        # trips[id] = trips[ikd][0:20]

        # sample train data
        for ts in trips[id]:
            tmp_train_time = train_time
            if len(ts) < train_time / 2:
                tmp_train_time = len(ts) * 2 - 1

            xtmp = x.loc[ts[0]:ts[0]+np.timedelta64(tmp_train_time, 's')]
            ytmp = y.loc[ts[0]:ts[0]+np.timedelta64(tmp_train_time, 's')]
            X_train = X_train.append(xtmp)
            Y_train = Y_train.append(ytmp)

        # sample test data
        tmp_test_time = test_time
        if len(ts) < test_time / 2:
            tmp_test_time = len(ts) * 2 - 1

        xtmp = x.loc[test_ts[0]:test_ts[0]+np.timedelta64(tmp_test_time, 's')]
        ytmp = y.loc[test_ts[0]:test_ts[0]+np.timedelta64(tmp_test_time, 's')]
        X_test = X_test.append(xtmp)
        Y_test = Y_test.append(ytmp)

    X_test.reset_index(drop=True, inplace=True)
    X_train.reset_index(drop=True, inplace=True)


    X_train = X_train.values
    X_test = X_test.values
    Y_train = Y_train.squeeze()
    Y_test = Y_test.squeeze()
    Y_train = Y_train.astype(int)
    Y_test = Y_test.astype(int)

    X_train = np.nan_to_num(X_train)
    X_test = np.nan_to_num(X_test)

    return X_train, X_test, Y_train, Y_test

def train_test_split_bremsdruck(data, test_size):
    columns = data.columns
    features = list(columns)
    features.remove('class')
    X_train = pd.DataFrame(columns=features)
    X_test = pd.DataFrame(columns=features)
    Y_train = pd.DataFrame(columns=['class'])
    Y_test = pd.DataFrame(columns=['class'])
    ids = data['class'].unique()
    for id in ids:
        rows = data.loc[data['class'] == id]

        r_rows = rows.loc[rows['can0_ESP_Bremsdruck_median'] > 0]
        count = len(r_rows)
        test_count = count * test_size
        test = r_rows.head(int(round(test_count)))
        X_test = X_test.append(test[features])
        Y_test = Y_test.append(test['class'].to_frame())
        train = rows.drop(test.index)
        X_train = X_train.append(train[features])
        Y_train = Y_train.append(train['class'].to_frame())

    X_test.reset_index(drop=True, inplace=True)
    X_train.reset_index(drop=True, inplace=True)

    X_train = X_train.values
    X_test = X_test.values
    Y_train = Y_train.squeeze()
    Y_test = Y_test.squeeze()
    Y_train = Y_train.astype(int)
    Y_test = Y_test.astype(int)

    X_train = np.nan_to_num(X_train)
    X_test = np.nan_to_num(X_test)

    return X_train, X_test, Y_train, Y_test
