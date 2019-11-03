import argparse
import pathlib
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib import style
from matplotlib.dates import DateFormatter
import numpy as np
from asammdf import MDF
import csv
import glob

import os
import sys

def print_ids(input_path):
  print('=====Driver IDs=====')
  ids = []
  for file in os.listdir(input_path):
    id = file.split('_')[1].split('.')[0]
    if id not in ids:
      ids.append(id)

  print('\n'.join(ids))
  print('count: %d' % len(ids))

def print_times(input_path):
  id_to_time = dict()
  for file in os.listdir(input_path):
    id = file.split('_')[1].split('.')[0]
    timestamp = file.split('_')[0]
    ts = int(timestamp)/1000000000

    if id not in id_to_time:
      id_to_time[id] = []

    id_to_time[id].append(ts)

  # print(id_to_time)

def plot_times(input_path):
  id_to_time = dict()
  for file in os.listdir(input_path):
    id = file.split('_')[1].split('.')[0][:5]
    timestamp = file.split('_')[0]
    ts = int(int(timestamp)/1000000000)

    if id not in id_to_time:
      id_to_time[id] = []

    id_to_time[id].append(datetime.fromtimestamp(ts))

  plt.figure(1)
  ax = plt.subplot()
  ax.xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))

  for key, data_list in id_to_time.items():
    plt.plot(np.array(data_list), np.array([key] * len(data_list)), label=key)

  plt.legend()
  plt.ylabel('Driver')
  plt.xlabel('Time')
  plt.title('Trips')

def join_files_and_ids(input_path):
  driver = dict()
  for file in os.listdir(input_path):
    id = file.split('_')[1].split('.')[0]
    timestamp = float(file.split('_')[0])
    with open(os.path.join(input_path, file)) as csv_file:
      csv_reader = list(csv.reader(csv_file, delimiter=','))
      last_timestamp = csv_reader[-1][0]
      try:
        last_timestamp = float(last_timestamp)
      except:
        continue
      if id not in driver:
        driver[id] = dict()
      if timestamp not in driver[id]:
        driver[id][timestamp] = []
      driver[id][timestamp].append(last_timestamp)

  # calculate min and max timestamps and delta for each driver
  for d in driver:
    for file_time in driver[d]:
      tmin = driver[d][file_time][0]
      tmax = driver[d][file_time][0]
      for t in driver[d][file_time]:
        tmin = min(tmin, t)
        tmax = max(tmax, t)


def print_n_plot_total_trip_time(trips):
  print('=====Total trip time=====')
  total_trip_times = []
  for d in trips:
    total_trip_time = 0
    for t in trips[d]:
      total_trip_time += float(t[-1]) - float(t[0])
    total_trip_time = (
        total_trip_time + 2 * 60 * 1000000000) / (60 * 60 * 1000000000)
    total_trip_times.append(total_trip_time)
    print('ID: %s, trip count: %d, total trip time: %f h' %
          (d[:5], len(trips[d]), total_trip_time))

  # plot it
  plt.figure(2)
  y_pos = np.arange(len(trips))
  x_lables = [('%s (%d)' % (t[:5], len(trips[t]))) for t in trips]
  plt.bar(y_pos, np.array(total_trip_times), align='center', alpha=0.5)
  plt.xticks(y_pos, x_lables)
  plt.ylabel('Total trip times [h]')
  plt.xlabel('Driver')
  plt.title('Total Trip Times')


def get_trips(input_path):
  driver = dict()
  trips = dict()
  max_trip_delta = 5 * 60 * 1000000000  # 5 minutes
  for file in os.listdir(input_path):
    id = file.split('_')[1].split('.')[0]
    timestamp = file.split('_')[0]
    if id not in driver:
        driver[id] = []
    driver[id].append(timestamp)

  for d in driver:
    driver[d].sort()
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

def print_days_of_trips(input_path):
  print('=====Days of trips=====')
  driver = dict()
  for file in os.listdir(input_path):
    id = file.split('_')[1].split('.')[0]
    timestamp = float(file.split('_')[0])
    if id not in driver:
      driver[id] = []
    driver[id].append(datetime.fromtimestamp(
        timestamp/1000000000).strftime('%d.%m.%Y'))
  
  for d in driver:
    # remove duplicates
    driver[d] = list(dict.fromkeys(driver[d]))
    print('Driver: %s, Days: %s' % (d[:5], ' '.join(driver[d])))

def plot_velocity(id, trip, path, i):
  data_points = []
  ts = []

  for t in trip:
    start_time = int(float(t) / 1000000000)
    file_name = os.path.join(path, '%s_%s.ChannelGroup_*_ESP_21:.csv' % (t, id))
    file = glob.glob(file_name)[0]
    with open(file) as csv_file:
      csv_reader = list(csv.reader(csv_file, delimiter=','))
      for row in csv_reader[1:]:
        x = start_time + float(row[0])
        ts.append(datetime.fromtimestamp(x))
        data_points.append(float(row[1]))

  plt.figure(i)
  ax = plt.subplot()
  ax.xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))
  plt.plot(np.array(ts), np.array(data_points))
  plt.ylabel('Velocity [km/h]')
  plt.xlabel('Time')
  plt.title('Velocity %s' % id[:5])

def signal_frequences(input_path):
  print('=====Signal frequences=====')
  file = os.listdir(input_path)[0]
  mdf_file = MDF(os.path.join(input_path, file))
  mdf_file = mdf_file.filter(['can0_LWI_Lenkradwinkel', 'can0_LWI_VZ_Lenkradwinkel', 'can0_ESP_Fahrer_bremst', 'can0_ESP_Bremsdruck', 'can0_MO_Fahrpedalrohwert_01', 'can0_MO_Kuppl_schalter', 'can0_MO_Drehzahl_01', 'can0_MO_Gangposition', 'can0_ESP_v_Signal', 'can0_ESP_HL_Fahrtrichtung', 'can0_ESP_HR_Fahrtrichtung'])
  signals = mdf_file.iter_channels(skip_master=True)
  sf = dict()
  count = 0
  for signal in mdf_file:
    f = len(signal.timestamps) / (signal.timestamps[-1] - signal.timestamps[0])
    sf[signal.name[5:]] = f
    print('%s: %.2f Hz' % (signal.name, f))
    count += len(signal.timestamps)

  # print('Count: %d' % count)
  plt.figure(4)
  plt.bar(range(len(sf)), list(sf.values()), align='center')
  plt.yticks(np.arange(0, max(sf.values()), 10))
  plt.ylabel('Frequency [Hz]')
  plt.xticks(range(len(sf)), list(sf.keys()), rotation='vertical')
  
  
def plot_all_trips(trips):
  print('=====Plot all trips=====')
  plt.figure(1)
  ax = plt.subplot()
  ax.xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))

  for d in trips:
    ts = []
    for trip in trips[d]:
      for t in trip:
        tt = datetime.fromtimestamp(int(int(t)/1000000000))
        ts.append(tt)
    plt.plot(ts[:-1], np.array([d[:5]] * len(ts[:-1])), 'o', markersize=1, label=d[:5])

  plt.legend()
  plt.ylabel('Driver')
  plt.xlabel('Time')
  plt.title('Trips')

def main():

  my_parser = argparse.ArgumentParser(description='Get information from files')
  my_parser.add_argument('-m', '--mf4-input',
                         action='store',
                         metavar='mf4_input',
                         type=str,
                         required=True,
                         help='Input mf4 file or directory')

  # Execute the parse_args() method
  args = my_parser.parse_args()
  mf4_input_path = args.mf4_input

  if not os.path.isdir(mf4_input_path):
    print('The mf4 input path specified is not a directory')
    sys.exit()

  # print_ids(csv_input_path)
  # print_times(csv_input_path)
  # plot_times(csv_input_path)
  # trips = get_trips(mf4_input_path)
  # print_n_plot_total_trip_time(trips)
  # plot_all_trips(trips)
  # print_days_of_trips(mf4_input_path)
  # i = 100
  # for d in trips:
  #   for trip in trips[d]:
  #     plot_velocity(d, trip, csv_input_path, i)
  #     i += 1

  signal_frequences(mf4_input_path)
  plt.show()
if __name__ == "__main__":
  main()
