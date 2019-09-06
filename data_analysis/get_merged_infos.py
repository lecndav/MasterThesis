import argparse
import pathlib
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib import style
from matplotlib.dates import DateFormatter
import numpy as np
from asammdf import MDF
import csv
import glob
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

import os
import sys


def plot_velocity(input_path, velocity_ecu):
  file_names = os.path.join(input_path, ('*_*_%s*.csv' % velocity_ecu))
  files = glob.glob(file_names)
  i = 100
  for file in files:
    file_name = os.path.split(file)[1]
    id = file_name.split('_')[1]
    ts = []
    data_points = []
    i += 1
    with open(file) as csv_file:
      csv_reader = list(csv.reader(csv_file, delimiter=','))
      for row in csv_reader[1:]:
        x = float(row[0]) / 1000000000
        ts.append(datetime.fromtimestamp(x))
        data_points.append(float(row[1]))

    plt.figure(i)
    ax = plt.subplot()
    ax.xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))
    plt.plot(np.array(ts), np.array(data_points))
    plt.ylabel('Velocity [km/h]')
    plt.xlabel('Time')
    plt.title('Velocity %s' % id[:5])


def main():

  my_parser = argparse.ArgumentParser(description='Get information from files')
  my_parser.add_argument('-i', '--input',
                         action='store',
                         metavar='input',
                         type=str,
                         required=True,
                         help='Input csv file or directory')

  # Execute the parse_args() method
  args = my_parser.parse_args()

  input_path = args.input

  if not os.path.isdir(input_path):
    print('The csv input path specified is not a directory')
    sys.exit()

  velocity_ecu = 'ESP_21'
  plot_velocity(input_path, velocity_ecu)
  plt.show()

if __name__ == "__main__":
  main()
