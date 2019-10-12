import argparse
import pathlib
import pandas
import os
import sys
import matplotlib.pyplot as plt
from datetime import datetime
from asammdf import MDF
from tsfresh import extract_features

interesting_signals = ['can0_LWI_Lenkradwinkel', 'can0_LWI_VZ_Lenkradwinkel', 'can0_ESP_Fahrer_bremst', 'can0_ESP_Bremsdruck',
                       'can0_MO_Drehzahl_01', 'can0_MO_Gangposition', 'can0_ESP_v_Signal',  'can0_ESP_HL_Fahrtrichtung', 'can0_ESP_HR_Fahrtrichtung', 'can0_LWI_VZ_Lenkradw_Geschw', 'can0_LWI_Lenkradw_Geschw', 'can0_ESP_Querbeschleunigung', 'can0_ESP_Laengsbeschl', 'can0_ESP_Gierrate', 'can0_ESP_VZ_Gierrate', 'can0_MO_Fahrpedalrohwert_01', 'can0_MO_Kuppl_schalter']

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


def to_hdf5(ts, id, mf4_dir, hdf_dir):
  hdf_file = os.path.join(hdf_dir, '%s.hdf' % id[:5])
  for t in ts:
    file = os.path.join(mf4_dir, '%s_%s.mf4' % (t, id))
    mdf_file = MDF(file)
    filtered_mdf = mdf_file.filter(interesting_signals)
    data = filtered_mdf.to_dataframe()
    data.index = (data.index * 1000000000 + float(t))
    data.index = data.index.values.astype('datetime64[ns]')
    data.index = pandas.to_datetime(data.index)
    data.to_hdf(hdf_file, id.replace('-', '_'), append=True)


def main():

  my_parser = argparse.ArgumentParser(description='Get information from files')
  my_parser.add_argument('-m', '--mdf-input',
                         action='store',
                         metavar='mdf_input',
                         type=str,
                         required=True,
                         help='Input mdf file or directory')

  my_parser.add_argument('-o', '--output',
                         action='store',
                         metavar='ouput',
                         type=str,
                         required=True,
                         help='HDF5 dir to write')

  my_parser.add_argument('-d', '--duration',
                         action='store',
                         metavar='duration',
                         type=str,
                         required=False,
                         help='Duration in minutes')

  my_parser.add_argument('-t', '--trips',
                         action='store',
                         metavar='trips',
                         type=str,
                         required=False,
                         help='Trip count')

  # Execute the parse_args() method
  args = my_parser.parse_args()

  mdf_input_path = args.mdf_input
  hdf_dir = args.output
  duration = None
  trip_count = None
  if args.duration:
    duration = int(args.duration)
  elif args.trips:
    trip_count = int(args.trips)
  else:
    print('Either sepcifiy duration or amount of trips')
    sys.exit(1)

  if not os.path.isdir(mdf_input_path):
    print('The mdf input path specified is not a directory')
    sys.exit()

  files = order_files(mdf_input_path)
  trips = get_trips(files)

  for id in trips:
    if duration:
      ts = files[id][:int(duration)]
    if trip_count:
      ts = trips[id][:trip_count]
      ts = [item for sublist in ts for item in sublist]

    to_hdf5(ts, id, mdf_input_path, hdf_dir)


main()
