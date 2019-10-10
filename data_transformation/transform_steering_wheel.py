import argparse
import pathlib
import pandas as pd
import os
import sys
import h5py
import numpy as np


def main():

  my_parser = argparse.ArgumentParser(description='Transform steering wheel.')
  my_parser.add_argument('-d', '--hdf5',
                         action='store',
                         metavar='hdf5_input',
                         type=str,
                         required=True,
                         help='Input hdf5 file')

  # Execute the parse_args() method
  args = my_parser.parse_args()

  hdf5_input = args.hdf5

  if not os.path.isfile(hdf5_input):
    print('The hdf5 input path specified is not a directory')
    sys.exit()

  data = pd.read_hdf(hdf5_input)
  data['lenkradwinkel_tmp'] = data.apply(lambda row: row['can0_LWI_Lenkradwinkel'] * -1 if int(row['can0_LWI_VZ_Lenkradwinkel']) else row['can0_LWI_Lenkradwinkel'], axis=1)
  data['can0_LWI_Lenkradwinkel'].drop()
  data['can0_LWI_VZ_Lenkradwinkel'].drop()

  data.rename({'lenkradwinkel_tmp': 'can0_LWI_Lenkradwinkel'})
  print(data.head())

main()
