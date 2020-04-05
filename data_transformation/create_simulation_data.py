import argparse
import pathlib
import pandas as pd
import os
import sys
import h5py
import yaml
import numpy as np
import time
from random import randint, shuffle
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'lib'))
from helper import get_trips_from_hdf, get_data_from_random_trips, get_data_from_nice_trips

def main():

  my_parser = argparse.ArgumentParser(description='Create simulation data')
  my_parser.add_argument('-i', '--input',
                         action='store',
                         metavar='hdf5_input',
                         type=str,
                         required=True,
                         help='Input file')

  my_parser.add_argument('-t', '--trips',
                         action='store',
                         metavar='trips',
                         type=str,
                         required=True,
                         help='Config file with trips')

  my_parser.add_argument('-o', '--output',
                         action='store',
                         metavar='output',
                         type=str,
                         required=True,
                         help='Output directory for simulation data and profile')

  # Execute the parse_args() method
  args = my_parser.parse_args()

  hdf5_input = args.input
  trips_file = args.trips
  output = args.output

  nice_trips = dict()
  with open(trips_file, 'r') as stream:
    try:
      nice_trips = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
      print(exc)

  data = pd.read_hdf(hdf5_input)
  id = hdf5_input.split('/')[-1].split('_')[0]

  for i in range(10):
    sim_data, nice_trips = get_data_from_nice_trips(data, nice_trips, 1)
    profile = data.drop(sim_data.index)

    output_dir = os.path.join(output, id, str(i))
    os.makedirs(output_dir, exist_ok=True)
    profile.to_hdf(os.path.join(output_dir, 'profile.hdf'), id)
    sim_data.to_hdf(os.path.join(output_dir, 'sim.hdf'), id)


main()
