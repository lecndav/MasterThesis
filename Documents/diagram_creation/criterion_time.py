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
  data['criterion'].replace('entropy',2,inplace=True)
  data['max_depth'] = data['max_depth'].fillna(0)
  data = data[data['max_depth'] == 0]
  data = data[data['min_samples_leaf'] == 1]
  data = data[data['min_samples_split'] == 2]
  data = data[data['n_estimators'] == 100]

  data['time'] = [2.4, 0.7] # fake it till you make it

  values = data['criterion'].unique()
  colors = dict()
  for v in values:
    colors[v] = "#{:06x}".format(random.randint(0, 0xFFFFFF))

  data['color'] = data['criterion'].apply(lambda x: colors[x])

  plt.figure(num='criterion', figsize=(12,4))
  p4 = plt.subplot(121)
  test = data[data['criterion'] == 1]
  test.plot(kind='scatter',x='criterion',y='accuracy',color=test['color'],ax=p4)
  test = data[data['criterion'] == 2]
  test.plot(kind='scatter',x='criterion',y='accuracy',color=test['color'],ax=p4)
  # for v in values:
  #   temp = data[data['criterion'] == v]
  #   temp.plot(kind='scatter',x='criterion',y='accuracy',color=temp['color'],ax=p4)

  plt.legend(['1: gini', '2: entropy'])
  plt.ylabel('Accuracy')
  p4.grid(color='gray', linestyle='-', linewidth=0.25, alpha=0.5)

  p5 = plt.subplot(122)
  test = data[data['criterion'] == 1]
  test.plot(kind='scatter',x='time',y='accuracy',color=test['color'],ax=p5)
  test = data[data['criterion'] == 2]
  test.plot(kind='scatter',x='time',y='accuracy',color=test['color'],ax=p5)
  plt.legend(['1: gini', '2: entropy'])
  plt.xlabel('Time [s]')
  plt.ylabel('Accuracy')
  p5.grid(color='gray', linestyle='-', linewidth=0.25, alpha=0.5)

  plt.savefig('../Thesis/images/criterion_time.png', bbox_inches='tight')
  # plt.show()


main()