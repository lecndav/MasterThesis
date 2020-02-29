import argparse
import pathlib
from asammdf import MDF

import os
import sys

def convert_to_csv(file, ouput):
  file_name = os.path.split(file)[-1].split('.')[0]
  print('processing %s...' % file_name)
  with MDF(file) as mdf_file:
    print(ouput + file_name)
    mdf_file.export('csv', ouput + file_name)

def main():

  my_parser = argparse.ArgumentParser(description='Convert MF4 files to csv')
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
      convert_to_csv(file, output_path)
  elif os.path.isfile(input_path):
    convert_to_csv(input_path, output_path)

if __name__ == "__main__":
  main()
