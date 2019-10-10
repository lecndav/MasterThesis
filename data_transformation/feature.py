import argparse
import pathlib
import pandas
import os
import h5py
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from asammdf import MDF
from tsfresh import extract_features


def main():

  my_parser = argparse.ArgumentParser(description='Get information from files')
  my_parser.add_argument('-d', '--hdf5',
                         action='store',
                         metavar='hdf5_input',
                         type=str,
                         required=True,
                         help='Input hdf5 file or directory')

  # Execute the parse_args() method
  args = my_parser.parse_args()

  hdf5_input_path = args.hdf5_input

  if not os.path.isdir(hdf5_input_path):
    print('The hdf5 input path specified is not a directory')
    sys.exit()

  for file in os.listdir(hdf5_input_path):
    with h5py.File(file, 'r') as f:
      # List all groups
      print("Keys: %s" % f.keys())
      a_group_key = list(f.keys())[0]

      # Get the data
      data = list(f[a_group_key])
      data = data.stack()
      data.index.rename(['time', 'id'], inplace=True)
      data = data.reset_index()
      extracted_features = extract_features(data, column_id='id', column_sort='time', n_jobs=10)
      impute(extracted_features)
      # features_filtered = select_features(extracted_features, y)
      print(extracted_features)


main()
