import argparse
import pathlib
import pandas as pd
import os
import sys
import h5py
import numpy as np


def main():

  my_parser = argparse.ArgumentParser(description='Transform steering wheel.')
  my_parser.add_argument('-i', '--input',
                         action='store',
                         metavar='hdf5_input',
                         type=str,
                         required=True,
                         help='Input directory with source hdf5 files')

  my_parser.add_argument('-o', '--output',
                         action='store',
                         metavar='hdf5_output',
                         type=str,
                         required=True,
                         help='Output directory')

  my_parser.add_argument('-s', '--window-size',
                         action='store',
                         metavar='windowsize',
                         type=str,
                         required=True,
                         help='Window size in ms')

  # Execute the parse_args() method
  args = my_parser.parse_args()

  hdf5_input = args.input
  hdf5_output = args.output
  window_size = args.window_size

  if not os.path.isdir(hdf5_input):
    print('The hdf5 input path specified is not a directory')
    sys.exit()

  if not os.path.isdir(hdf5_output):
    print('The hdf5 ouput path specified is not a directory')
    sys.exit()

  for file in os.listdir(hdf5_input):
    if not file.endswith('.hdf'):
      continue
    print('process %s' % file)
    data = pd.read_hdf(os.path.join(hdf5_input, file))
    column_names = list(data.head())

    data_mean = data.resample('%sL' % window_size).mean()
    new_column_names = dict()
    for n in column_names:
      new_column_names[n] = '%s_mean' % n
    data_mean = data_mean.rename(columns=new_column_names)

    data_std = data.resample('%sL' % window_size).std()
    new_column_names = dict()
    for n in column_names:
      new_column_names[n] = '%s_std' % n
    data_std = data_std.rename(columns=new_column_names)

    data_min = data.resample('%sL' % window_size).min()
    new_column_names = dict()
    for n in column_names:
      new_column_names[n] = '%s_min' % n
    data_min = data_min.rename(columns=new_column_names)

    data_max = data.resample('%sL' % window_size).max()
    new_column_names = dict()
    for n in column_names:
      new_column_names[n] = '%s_max' % n
    data_max = data_max.rename(columns=new_column_names)

    data_median = data.resample('%sL' % window_size).median()
    new_column_names = dict()
    for n in column_names:
      new_column_names[n] = '%s_median' % n
    data_median = data_median.rename(columns=new_column_names)

    data = pd.concat([data_mean, data_max, data_median, data_min, data_std], axis=1, sort=False)

    data.to_hdf(os.path.join(hdf5_output, file), file.split('.')[0])

main()
