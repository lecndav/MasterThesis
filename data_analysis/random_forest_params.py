import argparse
import pathlib
import pandas as pd
import os
import sys
import numpy as np
import csv


def main():

  my_parser = argparse.ArgumentParser(description='Analyse random forest parameter optimization')
  my_parser.add_argument('-i', '--input',
                         action='store',
                         metavar='file',
                         type=str,
                         required=True,
                         help='Input file')

  # Execute the parse_args() method
  args = my_parser.parse_args()

  file = args.file
  data = pd.read_csv(file)
  # print top accruracy
  # print top time
  # plot chart with x=time, y=accuracy

main()