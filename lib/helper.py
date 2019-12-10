import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from random import randint
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


def train_test_split(data, test_size):
  columns = data.columns
  features = list(columns)
  features.remove('class')
  x = data[features]
  y = data['class']
  y = y.to_frame()
  X_train = pd.DataFrame(columns=x.columns)
  X_test = pd.DataFrame(columns=x.columns)
  Y_train = pd.DataFrame(columns=['class'])
  Y_test = pd.DataFrame(columns=['class'])
  ids = data['class'].unique()
  for id in ids:
    rows = data.loc[data['class'] == id]
    rows = rows.loc[rows['can0_ESP_v_Signal_min'] < 1]
    rows = rows['can0_ESP_v_Signal_min']
    trips_start = list()
    first_time = rows.iloc[[0]].index[0]
    trips_start.append(first_time)
    last_time = first_time
    for row in rows.iteritems():
      diff = row[0] - last_time
      diff = diff.total_seconds()
      if diff > 20 * 60:
        trips_start.append(row[0])
        last_time = row[0]
    r = randint(0, len(trips_start)-2)
    start_test_data = trips_start[0]
    end_test_data = start_test_data + timedelta(seconds=test_size)
    start_test_data = start_test_data.strftime("%Y-%m-%d %H:%M:%S")
    end_test_data = end_test_data.strftime("%Y-%m-%d %H:%M:%S")
    xtmp = x.loc[start_test_data:end_test_data]
    ytmp = y.loc[start_test_data:end_test_data]
    X_test = X_test.append(xtmp)
    Y_test = Y_test.append(ytmp)

    plt.figure()
    xtmp['can0_ESP_v_Signal_mean'].plot()

  xtest_i = list(X_test.iloc[:].index)
  ytest_i = list(Y_test.iloc[:].index)
  X_train = x.drop(xtest_i)
  Y_train = y.drop(ytest_i)
  # X_test.reset_index(drop=True, inplace=True)
  # X_train.reset_index(drop=True, inplace=True)
  # X_train = X_train.sample(frac=1)
  # Y_train = Y_train.sample(frac=1)
  # X_test = X_test.sample(frac=1)
  # Y_test = Y_test.sample(frac=1)

  X_train = X_train.values
  X_test = X_test.values
  Y_train = Y_train.squeeze()
  Y_test = Y_test.squeeze()
  Y_train = Y_train.astype(int)
  Y_test = Y_test.astype(int)

  X_train = np.nan_to_num(X_train)
  X_test = np.nan_to_num(X_test)

  plt.show()

  return X_train, X_test, Y_train, Y_test
