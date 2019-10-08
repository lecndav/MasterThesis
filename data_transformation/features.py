import argparse
import pathlib
import pandas
import os
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

def process_trips(ts, id, dir):
  signal_speed = 'can0_ESP_v_Signal'
  d = None
  for t in ts:
    file = os.path.join(dir, '%s_%s.mf4' % (t, id))
    mdf_file = MDF(file)
    filtered_mdf = mdf_file.filter(interesting_signals)
    data = filtered_mdf.to_dataframe()
    data.index = (data.index * 1000000000 + float(t))
    data.index = data.index.values.astype('datetime64[ns]')
    data.index = pandas.to_datetime(data.index)
    if d is None:
      d = data
    else:
      d = d.append(data, sort=False)
  
  return d



def main():

  my_parser = argparse.ArgumentParser(description='Get information from files')
  my_parser.add_argument('-m', '--mdf-input',
                         action='store',
                         metavar='mdf_input',
                         type=str,
                         required=True,
                         help='Input mdf file or directory')

  # Execute the parse_args() method
  args = my_parser.parse_args()

  mdf_input_path = args.mdf_input

  if not os.path.isdir(mdf_input_path):
    print('The mdf input path specified is not a directory')
    sys.exit()

  trips = order_files(mdf_input_path)
  for id in trips:
    data = process_trips(trips[id][:1], id, mdf_input_path)
    data = data.stack()
    data.index.rename(['time', 'id'], inplace=True)
    data = data.reset_index()
    extracted_features = extract_features(data, column_id='id', column_sort='time')
    # impute(extracted_features)
    # features_filtered = select_features(extracted_features, y)
    print(extracted_features)
    break


main()
