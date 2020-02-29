import argparse
import pathlib
import pandas as pd
import os
import sys
import numpy as np
import csv
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import random
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})
rcParams['axes.spines.top'] = False
rcParams['axes.spines.right'] = False


def main():

    my_parser = argparse.ArgumentParser(
        description='Analyse feature importance')
    my_parser.add_argument('-i',
                           '--input',
                           action='store',
                           metavar='file',
                           type=str,
                           required=True,
                           help='Input directory')

    # Execute the parse_args() method
    args = my_parser.parse_args()
    data = pd.DataFrame()

    input_dir = args.input
    for file in os.listdir(input_dir):
        if not file.endswith('.csv'):
            continue
        t = pd.read_csv(os.path.join(input_dir, file))
        data = data.append(t, sort=True)

    signals = (list(set(data.columns) - set(['accuracy'])))
    data = (data[signals].mean(axis=0) * 100).sort_values(ascending=True).to_frame()

    with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more
        print(data)

    ax = data.plot(kind='barh', figsize=[5, 10], legend=False)
    plt.tight_layout()

    signals = data.T.columns
    signals = signals.map(lambda x: ('%s_%s' %
                                     (x.split('_')[2], '_'.join(x.split('_')[3:]))))
    ax.set_yticklabels(signals)
    ax.grid(color='gray', linestyle='-', linewidth=0.25, alpha=0.5)
    plt.xlabel('Importance [%]')

    # plt.show()
    plt.savefig('../Thesis/images/feature_perm_importance.png')


main()
