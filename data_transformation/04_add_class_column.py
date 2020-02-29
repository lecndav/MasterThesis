import argparse
import pathlib
import pandas as pd
import os
import sys
import h5py
import numpy as np


def main():

  my_parser = argparse.ArgumentParser(description='Add class column with driver id.')
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

  # Execute the parse_args() method
  args = my_parser.parse_args()

  hdf5_input = args.input
  hdf5_output = args.output

  if not os.path.isdir(hdf5_input):
    print('The hdf5 input path specified is not a directory')
    sys.exit()

  if not os.path.isdir(hdf5_output):
    print('The hdf5 ouput path specified is not a directory')
    sys.exit()

  i = 0
  for file in os.listdir(hdf5_input):
    if not file.endswith('.hdf'):
      continue
    print('process %s' % file)
    id = file.split('_')[0]
    data = pd.read_hdf(os.path.join(hdf5_input, file))
    data['class'] = id
    data.to_hdf(os.path.join(hdf5_output, file), id)
    i += 1


main()
