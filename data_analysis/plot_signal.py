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

  my_parser.add_argument('-s', '--signal',
                         action='store',
                         metavar='signal',
                         type=str,
                         required=True,
                         help='CAN signal to plot')

  # Execute the parse_args() method
  args = my_parser.parse_args()

  hdf5_input = args.hdf5
  signal = args.signal

  if not os.path.isfile(hdf5_input):
    print('The hdf5 input path specified is not a directory')
    sys.exit()

  data = pd.read_hdf(hdf5_input)

  if signal not in data.columns:
    print('Signal not available')
    sys.exit(1)

  data[signal].plot()
  plt.show()

main()
