import argparse
import pathlib
import pandas as pd
import os
import sys
import h5py
import yaml
import numpy as np
import random
import matplotlib.pyplot as plt
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'lib'))
from helper import get_trips_from_hdf, get_data_from_random_trips


def main():

  my_parser = argparse.ArgumentParser(description='Magic random forest classifier')
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

  # Execute the parse_args() method
  args = my_parser.parse_args()

  hdf5_input = args.input
  config_file = args.config

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
  nice_trips = dict()
  for id in trips:
    tdata = data[data['class'] == id]
    nice_trips['%d' % id] = []

    trip_starts = list(map(lambda trip: trip[0], trips[id]))
    trip_ends = list(map(lambda trip: trip[-1], trips[id]))

    for i, (start, end) in enumerate(zip(trip_starts, trip_ends)):
      duration = (end-start) / np.timedelta64(1, 's')
      mean = tdata['can0_ESP_v_Signal_mean'].loc[start:end].mean()
      if duration > 10*60 and mean < 90:
        nice_trips['%d' % id].append({'start': pd.Timestamp(start).strftime('%d.%m.%Y %H:%M:%S'), 'end': pd.Timestamp(end).strftime('%d.%m.%Y %H:%M:%S')})

  with open(config_file, 'w') as config:
    yaml.dump(nice_trips, config)

  # plt.figure()
  # ax = tdata['can0_ESP_v_Signal_mean'].plot()
  # for i, t in enumerate(trip_starts[id]):
    # ts = pd.Timestamp(t).strftime('%d.%m.%Y %H:%M:%S')
  #   ax.annotate('%s,%s' % (i, ts), (t, 0))

  # plt.show()

main()