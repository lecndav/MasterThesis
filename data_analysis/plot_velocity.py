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
  data['can0_ESP_v_Signal'].plot()
  plt.show()


main()
