import argparse
import pathlib
import pandas as pd
import os
import sys
import numpy as np
import csv
import matplotlib.pyplot as plt
import random
from matplotlib import rcParams

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
  data = data[data['min_samples_leaf'] == 1]
  data = data[data['min_samples_split'] == 2]

  # fake it till you make it
  data['time'] = [1.340942, 1.179480, 1.310942, 0.802915, 0.539031, 0.926197, 0.254825]

  values = data['n_estimators'].unique()
  colors = dict()
  for v in values:
    colors[v] = "#{:06x}".format(random.randint(0, 0xFFFFFF))

  data['color'] = data['n_estimators'].apply(lambda x: colors[x])

  plt.figure(num='n_estimators', figsize=(12,4))
  p4 = plt.subplot(121)
  for v in values:
    temp = data[data['n_estimators'] == v]
    ax = temp.plot(kind='scatter',x='n_estimators',y='accuracy',color=temp['color'],ax=p4)
    ax.grid(color='gray', linestyle='-', linewidth=0.25, alpha=0.5)
    # mean = temp['accuracy'].mean()
    # ax.plot(v, mean, 'xk')

  plt.legend(data['n_estimators'])

  p5 = plt.subplot(122)
  for v in values:
    temp = data[data['n_estimators'] == v]
    ax = temp.plot(kind='scatter',x='time',y='accuracy',color=temp['color'],ax=p5)
    ax.grid(color='gray', linestyle='-', linewidth=0.25, alpha=0.5)

  plt.xlabel('Time [s]')
  plt.ylabel('Accuracy')
  plt.legend(data['n_estimators'])

  # plt.show()
  plt.savefig('../Thesis/images/n_estimators.png', bbox_inches='tight')


main()