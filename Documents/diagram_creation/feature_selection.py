import argparse
import pathlib
import pandas as pd
import os
import sys
import numpy as np
import csv
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import random
from matplotlib import rcParams

rcParams['axes.spines.top'] = False
rcParams['axes.spines.right'] = False


def main():

  my_parser = argparse.ArgumentParser(description='Analyse feature importance')
  my_parser.add_argument('-i', '--input',
                         action='store',
                         metavar='file',
                         type=str,
                         required=True,
                         help='Input directory')

  # Execute the parse_args() method
  args = my_parser.parse_args()
  data = pd.DataFrame()

  input_dir = args.input
  for file in os.listdir(input_dir):
    if not file.endswith('.csv'):
      continue
    t = pd.read_csv(os.path.join(input_dir, file))
    a = t[t['feature_count'] == 64].values[0]
    # if a[0] < 0.81:
    #   continue
    data = data.append(t, sort=True)


  ax = data.plot(x='feature_count', y='accuracy', kind='scatter', figsize=(15,8))
  ax.set_xlabel('Feature amount')
  ax.set_ylabel('Accuracy')
  ax.grid(color='gray', linestyle='-', linewidth=0.25, alpha=0.5)

  accs = []
  fc = []
  for a in data['feature_count'].unique():
    t = data[data['feature_count']==a].mean()
    accs.append(t['accuracy'])
    fc.append(t['feature_count'])

  plt.plot(fc, accs, color='red')
  a = Line2D([0], [0], color='red', linewidth=2)
  plt.legend([a], ['average'])

  # plt.show()
  plt.savefig('../Thesis/images/feature_selection.png', bbox_inches='tight')

main()
