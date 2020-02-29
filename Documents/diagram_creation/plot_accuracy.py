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

  my_parser = argparse.ArgumentParser(description='Plot accuracy from file')
  my_parser.add_argument('-i', '--input',
                         action='store',
                         metavar='file',
                         type=str,
                         required=True,
                         help='Input file')

  # Execute the parse_args() method
  args = my_parser.parse_args()

  data = pd.read_csv(args.input)
  data['x'] = range(1, len(data)+1)
  ax = data.plot(kind='scatter',x='x',y='accuracy')

  ax.spines['top'].set_visible(False)
  ax.spines['right'].set_visible(False)
  ax.grid(color='gray', linestyle='-', linewidth=0.25, alpha=0.5)
  plt.xlabel('Try')
  plt.ylabel('Accuracy')
  plt.savefig('../Thesis/images/rf_accuracy.png', bbox_inches='tight')
#   plt.show()


main()