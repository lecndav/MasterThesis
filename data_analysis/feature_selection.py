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
    data = data.append(t, sort=True)

  data.plot(x='feature_count', y='accuracy', kind='scatter')
  plt.show()

main()
