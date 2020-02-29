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
  data = data[data['accuracy'] > 0.7]
  data['criterion'].replace('gini',1,inplace=True)
  data['max_depth'] = data['max_depth'].fillna(0)
  data = data[data['criterion'] == 1]
  data = data[data['min_samples_leaf'] == 1]
  data = data[data['n_estimators'] == 100]
  data = data[data['min_samples_split'] == 2]

  values = data['max_depth'].unique()
  colors = dict()
  for v in values:
    colors[v] = "#{:06x}".format(random.randint(0, 0xFFFFFF))

  data['color'] = data['max_depth'].apply(lambda x: colors[x])

  p4 = plt.subplot(111)
  for v in values:
    temp = data[data['max_depth'] == v]
    ax = temp.plot(kind='scatter',x='max_depth',y='accuracy',color=temp['color'],ax=p4)
    # mean = temp['accuracy'].mean()
    # ax.plot(v, mean, 'xk')
  plt.yticks(np.arange(0.85,0.94, 0.01))
  plt.ylabel('Accuracy')
  p4.grid(color='gray', linestyle='-', linewidth=0.25, alpha=0.5)

  # plt.show()
  plt.savefig('../Thesis/images/max_depth.png', bbox_inches='tight')


main()