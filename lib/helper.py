import os
import pandas as pd
from random import randint

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
  ids = data['class'].unique()
  for id in ids:
    rows = data.loc[data['class'] == id]
    rows = rows.loc[rows['can0_ESP_v_Signal_min'] < 1]
    rows = rows['can0_ESP_v_Signal_min']
    first_rows = list()
    first_val = rows.iloc[0]
    first_time = rows.iloc[[0]].index[0]
    first_rows.append((first_time, first_val))
    last_first = first_time
    for row in rows.iteritems():
      diff = row[0] - last_first
      diff = diff.total_seconds()
      if diff > 10 * 60:
        first_rows.append((row[0], row[1]))
        last_first = row[0]
    


  # features = list(columns)
  # features.remove('class')
  # x = data[features]
  # y = data['class']
  # X_train = pd.DataFrame(columns=x.columns)
  # X_test = pd.DataFrame(columns=x.columns)
  # y_train = pd.DataFrame(columns=['class'])
  # y_test = pd.DataFrame(columns=['class'])
