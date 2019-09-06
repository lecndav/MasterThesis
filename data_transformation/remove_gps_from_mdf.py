import argparse
import pathlib
from asammdf import MDF

import os
import sys

gps_signals = ['can1_NP_LatDegree',
               'can1_NP_LongDegree', 'can1_NP_Fix', 'can1_ND_Heading', 'can1_NP_Altitude']

def remove_gps(mf4_file):
  with MDF(mf4_file) as mdf_file:
    print("processing " + mf4_file)
    signals_iterator = mdf_file.iter_channels(skip_master=False)
    signals = []
    for signal in signals_iterator:
      signals.append(signal.name)

    # remove gps_signals from signal list
    new_signals = list((x for x in signals if x not in set(gps_signals)))
    new_mdf = mdf_file.filter(new_signals)
    return new_mdf

def main():

  my_parser = argparse.ArgumentParser(description='Remove GPS data from mf4 files and convert it to CSV')
  my_parser.add_argument('-i', '--input',
                         action='store',
                         metavar='input',
                         type=str,
                         required=True,
                         help='Input file or directory')

  my_parser.add_argument('-o', '--output',
                         action='store',
                         metavar='output',
                         type=str,
                         required=True,
                         help='Output directory')

  # Execute the parse_args() method
  args = my_parser.parse_args()

  input_path = args.input
  output_path = args.output

  if not os.path.isdir(input_path) and not os.path.isfile(input_path):
    print('The input path specified does not exist')
    sys.exit()

  if not os.path.isdir(output_path):
    print('The output path specified does not exist')
    sys.exit()

  if os.path.isdir(input_path):
    file_names = os.listdir(input_path)
    for file_name in file_names:
      file = os.path.join(input_path, file_name)
      new_file = remove_gps(file)
      new_file_name = os.path.join(output_path, file_name)
      new_file.save(new_file_name)
  elif os.path.isfile(input_path):
    new_file = remove_gps(input_path)
    file_name = os.path.split(input_path)[-1]
    new_file_name = os.path.join(output_path, file_name)
    new_file.save(new_file_name)


if __name__ == "__main__":
  main()
