import argparse
import pathlib
import pandas as pd
import os
import sys
import h5py
import yaml
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams

rcParams['axes.spines.top'] = False
rcParams['axes.spines.right'] = False


def main():

  my_parser = argparse.ArgumentParser(description='Magic random forest classifier')
  my_parser.add_argument('-i', '--input',
                         action='store',
                         metavar='hdf5_input',
                         type=str,
                         required=True,
                         help='Input directory with source hdf5 files')

  # Execute the parse_args() method
  args = my_parser.parse_args()

  hdf5_input = args.input

  if not os.path.isdir(hdf5_input):
    print('The hdf5 input path specified is not a directory')
    sys.exit()

  xs = [0,0,0,1,1,1,2,2,2]
  ys = [0,1,2,0,1,2,0,1,2]
  i = 0
  fig, axs = plt.subplots(3, 3, figsize=(12,8))
  for file in os.listdir(hdf5_input):
    if not file.endswith('.hdf'):
      continue

    data = pd.read_hdf(os.path.join(hdf5_input, file))

    axs[xs[i], ys[i]].plot(data['can0_MO_Gangposition_mean'])
    axs[xs[i], ys[i]].tick_params(axis='y')
    axs[xs[i], ys[i]].grid(color='gray', linestyle='-', linewidth=0.25, alpha=0.5)

    axs[xs[i], ys[i]].set_title('Driver %d' % (i+1))
    axs[xs[i], ys[i]].get_xaxis().set_visible(False)

    i += 1


  plt.savefig('../Thesis/images/gear_position.png', bbox_inches='tight')
  # plt.show()


main()
