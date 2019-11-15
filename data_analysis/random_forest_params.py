import argparse
import pathlib
import pandas as pd
import os
import sys
import numpy as np
import csv
import matplotlib.pyplot as plt
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


  data = data.sort_values(['accuracy'], ascending=True)
  data = data.iloc[0:200]
  data['criterion'].replace('gini',1,inplace=True)
  data['criterion'].replace('entropy',2,inplace=True)
  data = data[data['criterion'] == 1]

  param_names = ['min_samples_leaf', 'n_estimators', 'max_depth']

  for name in param_names:
    values = data[name].unique()
    colors = dict()
    for v in values:
      colors[v] = "#{:06x}".format(random.randint(0, 0xFFFFFF))

    data['color'] = data[name].apply(lambda x: colors[x])

    plt.figure(num=name)
    p1 = plt.subplot(221)
    est_value_count = data['n_estimators'].value_counts()
    for val, count in est_value_count.items():
      y = data[data['n_estimators'] == val].iloc[0].accuracy
      p1.annotate(str(count), (val, y))
    plt.title('Estimators')
    data.plot(kind='scatter',x='n_estimators',y='accuracy',color=data['color'], ax=p1)

    p2 = plt.subplot(222)
    max_d_value_count = data['max_depth'].value_counts()
    for val, count in max_d_value_count.items():
      y = data[data['max_depth'] == val].iloc[0].accuracy
      p2.annotate(str(count), (val, y))
    plt.title('Max depth')
    data.plot(kind='scatter',x='max_depth',y='accuracy',color=data['color'],ax=p2)

    p3 = plt.subplot(223)
    criterion_value_count = data['min_samples_leaf'].value_counts()
    for val, count in criterion_value_count.items():
      y = data[data['min_samples_leaf'] == val].iloc[0].accuracy
      p3.annotate(str(count), (val, y))
    plt.title('min_samples_leaf')
    data.plot(kind='scatter',x='min_samples_leaf',y='accuracy',color=data['color'],ax=p3)

    p4 = plt.subplot(224)
    plt.title('Time')
    data.plot(kind='scatter',x='time',y='accuracy',color=data['color'],ax=p4)
  
  plt.show()


main()