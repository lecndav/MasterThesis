import argparse
import pathlib
import pandas as pd
import os
import sys
import numpy as np
import csv
import matplotlib.pyplot as plt
from matplotlib import rcParams
import random

rcParams['axes.spines.top'] = False
rcParams['axes.spines.right'] = False

def main():

  my_parser = argparse.ArgumentParser(description='Analyse random forest parameter optimization')
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
    data = data.append(t)

  data = data.sort_values(['accuracy'], ascending=False)
  data['criterion'].replace('gini',1,inplace=True)
  data['max_depth'] = data['max_depth'].fillna(0)
  data = data[data['criterion'] == 1]
  data = data[data['max_depth'] == 0]
  data = data[data['n_estimators'] == 100]
  data = data[data['min_samples_leaf'] == 1]

  values = data['min_samples_split'].unique()
  colors = dict()
  for v in values:
    colors[v] = "#{:06x}".format(random.randint(0, 0xFFFFFF))

  data['color'] = data['min_samples_split'].apply(lambda x: colors[x])

  p4 = plt.subplot(111)
  for v in values:
    temp = data[data['min_samples_split'] == v]
    ax = temp.plot(kind='scatter',x='min_samples_split',y='accuracy',color=temp['color'],ax=p4)
    ax.grid(color='gray', linestyle='-', linewidth=0.25, alpha=0.5)
    # mean = temp['accuracy'].mean()
    # ax.plot(v, mean, 'xk')

  plt.xticks(range(0,22,2))
  # plt.show()
  plt.ylabel('Accuracy')
  plt.savefig('../Thesis/images/min_samples_split.png', bbox_inches='tight')


main()