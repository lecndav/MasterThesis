import argparse
import pathlib
import pandas as pd
import os
import sys
import h5py
import yaml
import numpy as np
import time
from random import randint, shuffle


def main():

    my_parser = argparse.ArgumentParser(description='Simulates HDF files')
    my_parser.add_argument('-c',
                           '--config',
                           action='store',
                           metavar='config',
                           type=str,
                           required=True,
                           help='Config file')

    args = my_parser.parse_args()
    config_file = args.config

    print('Starting hdf-simulator.py')

    config = dict()
    with open(config_file, 'r') as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    if not os.path.isfile(config['input_file']):
        print('Input file does not exist')
        exit(1)

    if not os.path.isdir(config['output_dir']):
        print('Directory with profiles does not exist')
        exit(1)

    data = pd.read_hdf(config['input_file'])
    print('Loaded driver data')

    duration = np.timedelta64(500, 's')
    for i in range(int(len(data) / 30)):
        start = data.index[i * 30]
        tmp = data[start:start + duration]
        output_file = os.path.join(config['output_dir'], str(start.value) + '.hdf')
        print(output_file)
        tmp.to_hdf(output_file,'driverX')
        print('Provided 1 minute data')
        time.sleep(5)


main()