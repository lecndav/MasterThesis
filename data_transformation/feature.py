import argparse
import pathlib
import pandas as pd
import os
import sys
import h5py
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from asammdf import MDF
from tsfresh import extract_features
from tsfresh.utilities.dataframe_functions import impute


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

  hdf5_input = args.hdf5

  if not os.path.isfile(hdf5_input):
    print('The hdf5 input path specified is not a directory')
    sys.exit()

  # id = hdf5_input.split('/')[-1].split('.')[0]
  data = pd.read_hdf(hdf5_input)
  data = data.stack()
  data.index.rename(['time', 'id'], inplace=True)
  data = data.reset_index()
  extracted_features = extract_features(data[:1000000], column_id='id', column_sort='time', n_jobs=10)
  impute(extracted_features)
  # features_filtered = select_features(extracted_features, y)
  print(extracted_features)


main()
