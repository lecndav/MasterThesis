import argparse
import pandas as pd
import numpy as np
import random
import os
import sys
import yaml
import time
from datetime import datetime
from asammdf import MDF


def filter_mdf(file, signals):
    mdf_file = MDF(file)
    # Lenkradwinkel
    lenkradwinkel = mdf_file.get('can0_LWI_Lenkradwinkel')
    samples = list(lenkradwinkel.samples)
    vz_samples = list(mdf_file.get('can0_LWI_VZ_Lenkradwinkel').samples)
    for i in range(0, len(samples)):
        if not int(vz_samples[i]):
            samples[i] = samples[i] * -1
    lenkradwinkel.samples = np.asarray(samples)

    # Lenkradwinkel geschw.
    lenkrad_gesch = mdf_file.get('can0_LWI_Lenkradw_Geschw')
    samples = list(lenkrad_gesch.samples)
    vz_samples = list(mdf_file.get('can0_LWI_VZ_Lenkradw_Geschw').samples)
    for i in range(0, len(samples)):
        if not int(vz_samples[i]):
            samples[i] = samples[i] * -1
    lenkrad_gesch.samples = np.asarray(samples)

    # Gierrate
    gierrate = mdf_file.get('can0_ESP_Gierrate')
    samples = list(gierrate.samples)
    vz_samples = list(mdf_file.get('can0_ESP_VZ_Gierrate').samples)
    for i in range(0, len(samples)):
        if not int(vz_samples[i]):
            samples[i] = samples[i] * -1
    gierrate.samples = np.asarray(samples)

    # filter file with VZ signals
    filtered_mdf = mdf_file.filter(signals)
    return filtered_mdf


def resample(data, window_size):
    column_names = list(data.head())

    data_mean = data.resample('%sL' % window_size).mean()
    new_column_names = dict()
    for n in column_names:
        new_column_names[n] = '%s_mean' % n
    data_mean.rename(columns=new_column_names, inplace=True)

    data_std = data.resample('%sL' % window_size).std()
    new_column_names = dict()
    for n in column_names:
        new_column_names[n] = '%s_std' % n
    data_std.rename(columns=new_column_names, inplace=True)

    data_min = data.resample('%sL' % window_size).min()
    new_column_names = dict()
    for n in column_names:
        new_column_names[n] = '%s_min' % n
    data_min.rename(columns=new_column_names, inplace=True)

    data_max = data.resample('%sL' % window_size).max()
    new_column_names = dict()
    for n in column_names:
        new_column_names[n] = '%s_max' % n
    data_max.rename(columns=new_column_names, inplace=True)

    data_median = data.resample('%sL' % window_size).median()
    new_column_names = dict()
    for n in column_names:
        new_column_names[n] = '%s_median' % n
    data_median.rename(columns=new_column_names, inplace=True)

    data = pd.concat([data_mean, data_max, data_median, data_min, data_std],
                     axis=1,
                     sort=False)
    data.dropna(inplace=True)
    return data


def mdf_to_df(mdf_file, timestamp):
    data = mdf_file.to_dataframe()
    data.index = (data.index * 1000000000 + float(timestamp))
    data.index = data.index.values.astype('datetime64[ns]')
    data.index = pd.to_datetime(data.index)
    return data


def main():

    my_parser = argparse.ArgumentParser(
        description='Preprocesses mdf data and stores it in hdf5 file')
    my_parser.add_argument('-c',
                           '--config',
                           action='store',
                           metavar='config',
                           type=str,
                           required=True,
                           help='Configuration file')

    my_parser.add_argument('-r',
                           action='store',
                           metavar='reset',
                           type=bool,
                           default=False,
                           help='Remove files from output dir')

    args = my_parser.parse_args()
    config_file = args.config
    reset = args.reset

    print('Starting data-preprocessor.py')

    config = dict()
    with open(config_file, 'r') as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    if not os.path.isdir(config['measured_output']):
        print('Measured directory does not exist')
        exit(1)

    if not os.path.isdir(config['output_dir']):
        print('Output directory does not exist')
        exit(1)

    if reset:
        os.system('rm -rf %s/*', config['output_dir'])
        os.system('rm -rf %s/*', config['measured_output'])

    while True:
        for file in os.listdir(config['measured_output']):
            print('New data available...')
            if not file.endswith('.mf4'):
                continue
            timestamp = file.split('_')[0]
            mdf_file = filter_mdf(
                os.path.join(config['measured_output'], file),
                config['signals'])
            df = mdf_to_df(mdf_file, timestamp)
            df = resample(df, config['window_size'])
            df = df[df['can0_ESP_v_Signal_max'] != 0]
            outfile = os.path.join(config['output_dir'], timestamp, '.hdf')
            df.to_hdf(outfile, 'driverX', append=True)

            print('Processed %s' % outfile)
            # move file to backup
            os.rename(os.path.join(config['measured_output'], file),
                      os.path.join(config['backup_output'], file))

        time.sleep(5)


main()