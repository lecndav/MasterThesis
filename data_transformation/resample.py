import argparse
import pathlib
import pandas as pd
import os
import sys
import h5py
import numpy as np


def m_rename(data, postfix):
    new_column_names = dict()
    column_names = list(data.head())
    for n in column_names:
        new_column_names[n] = '%s_%s' % (n, postfix)
    data.rename(columns=new_column_names, inplace=True)

    return data


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
    N = 3 * 10
    ov = 6

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

        data.drop('class', inplace=True, axis=1)
        signals = list(data.columns)

        data['group'] = data.index.to_series().diff().gt('300sec').cumsum()
        groups = data['group'].unique()

        new_data = pd.DataFrame()
        for g in groups:
            tdata = data[data['group'] == g]
            tdata.drop('group', axis=1, inplace=True)
            tdata = tdata.resample('100L').mean()
            median_data = pd.concat([tdata.shift(i).iloc[::N] for i in range(-ov, N+ov)], axis=1).groupby(level=0, axis=1).median()
            mean_data = pd.concat([tdata.shift(i).iloc[::N] for i in range(-ov, N+ov)], axis=1).groupby(level=0, axis=1).mean()
            min_data = pd.concat([tdata.shift(i).iloc[::N] for i in range(-ov, N+ov)], axis=1).groupby(level=0, axis=1).min()
            max_data = pd.concat([tdata.shift(i).iloc[::N] for i in range(-ov, N+ov)], axis=1).groupby(level=0, axis=1).max()
            std_data = pd.concat([tdata.shift(i).iloc[::N] for i in range(-ov, N+ov)], axis=1).groupby(level=0, axis=1).std()

            median_data = m_rename(median_data, 'median')
            mean_data = m_rename(mean_data, 'mean')
            min_data = m_rename(min_data, 'min')
            max_data = m_rename(max_data, 'max')
            std_data = m_rename(std_data, 'std')
            t_data = pd.concat(
                [median_data, mean_data, min_data, max_data, std_data],
                axis=1,
                sort=False)
            t_data.dropna(inplace=True)
            new_data = new_data.append(t_data)


        new_data['class'] = file.split('_')[0]
        new_data.to_hdf(os.path.join(hdf5_output, file), file.split('.')[0])


main()
