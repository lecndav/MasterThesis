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


def get_data_from_nice_trips(data, nice_trips, count):
    frames = []
    for id in nice_trips:
        for i in range(count):
            if len(nice_trips[id]) == 0:
                break

            r = randint(0, len(nice_trips) - 1)
            trip = nice_trips[id][r]
            del nice_trips[id][r]
            tdata = data[data['class'] == int(id)]
            frames.append(tdata.loc[trip['start']:trip['end']])

    return pd.concat(frames, sort=False), nice_trips


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

    while True:
        tdata, _ = get_data_from_nice_trips(data, config['trips'], 1)
        duration = np.timedelta64(60, 's')
        for i in range(int(len(tdata) / 30)):
            start = tdata.index[i * 30]
            tmp = tdata[start:start + duration]
            tmp.to_hdf(
                os.path.join(config['output_dir'], str(start.value), '.hdf'),
                'driverX')
            print('Provided 1 minute data')
            time.sleep(60)


main()