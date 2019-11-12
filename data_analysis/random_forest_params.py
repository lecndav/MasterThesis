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


  data = data.sort_values(['accuracy'], ascending=False)
  data = data.iloc[0:50]
  data['criterion'].replace('gini',1,inplace=True)
  data['criterion'].replace('entropy',2,inplace=True)

  param_names = ['criterion', 'n_estimators', 'max_depth']

  for name in param_names:
    values = data[name].unique()
    colors = dict()
    for v in values:
      colors[v] = "#{:06x}".format(random.randint(0, 0xFFFFFF))

    data['color'] = data[name].apply(lambda x: colors[x])

    plt.figure(num=name)
    p1 = plt.subplot(221)
    plt.title('Estimators')
    data.plot(kind='scatter',x='n_estimators',y='accuracy',color=data['color'], ax=p1)

    p2 = plt.subplot(222)
    plt.title('Max depth')
    data.plot(kind='scatter',x='max_depth',y='accuracy',color=data['color'],ax=p2)

    p3 = plt.subplot(223)
    plt.title('Criterion')
    data.plot(kind='scatter',x='criterion',y='accuracy',color=data['color'],ax=p3)

    p4 = plt.subplot(224)
    plt.title('Time')
    data.plot(kind='scatter',x='time',y='accuracy',color=data['color'],ax=p4)
  
  plt.show()


main()