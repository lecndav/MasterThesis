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

  data['accuracy'] = data['accuracy'].round(6)
  data.drop_duplicates('accuracy', inplace=True)
  data = data.sort_values(['accuracy'], ascending=False)
  data['criterion'].replace('gini',1,inplace=True)
  data['criterion'].replace('entropy',2,inplace=True)
  values = data['accuracy'].unique()
  colors = dict()
  for v in values:
    colors[v] = "#{:06x}".format(random.randint(0, 0xFFFFFF))

  data['color'] = data['accuracy'].apply(lambda x: colors[x])
  data['x'] = range(0, len(data))

  data.plot(kind='scatter',x='x',y='accuracy',color=data['color'])

  # plt.savefig('../Thesis/images/everything.png', bbox_inches='tight')
  plt.show()


main()