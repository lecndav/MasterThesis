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


def main():

  my_parser = argparse.ArgumentParser(description='Get information from files')
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
  test = data.loc['2019-07-13 10:54:58':'2019-07-13 11:01:00']
  vz = test['can0_LWI_VZ_Lenkradwinkel']
  vz = vz.apply(lambda x: -1 if x is 0 else x)
  fig, ax1 = plt.subplots()
  ax1.plot(test['can0_LWI_Lenkradwinkel'])
  ax2 = ax1.twinx()
  ax2.plot(vz, color='red')
  ax2.set_ylim(-5,5)
  plt.show()

main()
