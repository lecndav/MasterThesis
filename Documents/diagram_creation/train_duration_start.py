import sys
import os
import numpy as np
import pandas as pd
import matplotlib.pylab as plt
from matplotlib.lines import Line2D
import csv
import argparse
from matplotlib import rcParams

rcParams['axes.spines.top'] = False
rcParams['axes.spines.right'] = False

def main():

  my_parser = argparse.ArgumentParser(description='Plot accuracy from file')
  my_parser.add_argument('-i', '--input',
                         action='store',
                         metavar='file',
                         type=str,
                         required=True,
                         help='Input file')

  # Execute the parse_args() method
  args = my_parser.parse_args()

  file = args.input
  data = pd.read_csv(file)
  data = data[data['accuracy'] > 0.8]
  ax = data.plot(kind='scatter',x='duration',y='accuracy', figsize=(8,6))
  ax.set_xlabel('Training time [m]')
  ax.grid(color='gray', linestyle='-', linewidth=0.25, alpha=0.5)
  # x = range(12,41)
  # y = np.arange(0.90, 0.86, -0.0014)
  # plt.plot(x, y, color='red')

  accs = []
  ds = []
  for a in data['duration'].unique():
    t = data[data['duration']==a].mean()
    accs.append(t['accuracy'])
    ds.append(t['duration'])

  plt.plot(ds, accs, color='red')

  a = Line2D([0], [0], color='red', linewidth=2)
  plt.legend([a], ['average'])
  plt.ylabel('Accuracy')

  # plt.show()
  plt.savefig('../Thesis/images/train_duration_start.png', bbox_inches='tight')

main()
