import argparse
import pathlib
import pandas as pd
import os
import sys
import h5py
import numpy as np

gangpos = [
    'can0_MO_Gangposition_std', 'can0_MO_Gangposition_median',
    'can0_MO_Gangposition_mean', 'can0_MO_Gangposition_max',
    'can0_MO_Gangposition_max'
]


def main():

    my_parser = argparse.ArgumentParser(
        description='Transform steering wheel.')
    my_parser.add_argument('-i',
                           '--input',
                           action='store',
                           metavar='hdf5_input',
                           type=str,
                           required=True,
                           help='Input directory with source hdf5 files')

    my_parser.add_argument('-o',
                           '--output',
                           action='store',
                           metavar='hdf5_output',
                           type=str,
                           required=True,
                           help='Output directory')


    # Execute the parse_args() method
    args = my_parser.parse_args()

    hdf5_input = args.input
    hdf5_output = args.output

    if not os.path.isdir(hdf5_input):
        print('The hdf5 input path specified is not a directory')
        sys.exit()

    if not os.path.isdir(hdf5_output):
        print('The hdf5 ouput path specified is not a directory')
        sys.exit()

    for file in os.listdir(hdf5_input):
        if not file.endswith('.hdf'):
            continue
        print('process %s' % file)
        data = pd.read_hdf(os.path.join(hdf5_input, file))
        data.drop(gangpos, axis=1)
        data.to_hdf(os.path.join(hdf5_output, file), file.split('.')[0])


main()
