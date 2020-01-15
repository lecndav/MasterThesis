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
  my_parser.add_argument('-c', '--csv-file',
                         action='store',
                         metavar='file',
                         type=str,
                         required=True,
                         help='Input csv file')

  # Execute the parse_args() method
  args = my_parser.parse_args()
  file = args.csv_file

  data = pd.read_csv(file)

  data.plot(x='duration', y='accuracy', kind='scatter')
  plt.show()

main()
