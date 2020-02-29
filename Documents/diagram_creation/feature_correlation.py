import argparse
import pathlib
import pandas as pd
import os
import sys
import numpy as np
import csv
from scipy.stats import spearmanr, pearsonr
from scipy.cluster import hierarchy
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import random
from matplotlib import rcParams
from mpl_toolkits.axes_grid1 import make_axes_locatable
rcParams.update({'figure.autolayout': True})


def main():

    my_parser = argparse.ArgumentParser(description='Get information from files')
    my_parser.add_argument('-i', '--input',
                            action='store',
                            metavar='hdf5_input',
                            type=str,
                            required=True,
                            help='Input dir')

    # Execute the parse_args() method
    args = my_parser.parse_args()

    hdf5_input = args.input

    frames = []
    if not os.path.isdir(hdf5_input):
        print('The hdf5 input path specified is not a directory')
        sys.exit()

    for file in os.listdir(hdf5_input):
        if not file.endswith('.hdf'):
            continue

        data = pd.read_hdf(os.path.join(hdf5_input, file))
        frames.append(data)
        # break

    data = pd.concat(frames, sort=False)

    features = (list(set(data.columns) - set(['class'])))
    X = data[features]

    fig, (ax1) = plt.subplots(1, 1, figsize=(15, 15))
    corr = spearmanr(X).correlation
    corr_linkage = hierarchy.ward(corr)
    dendro = hierarchy.dendrogram(corr_linkage,
                                labels=features,
                                no_plot=True,
                                leaf_rotation=90)
    dendro_idx = np.arange(0, len(dendro['ivl']))


    lables = dendro['ivl']
    lables = list(map(lambda x: ('%s' % ('_'.join(x.split('_')[2:]))),lables))

    ims = ax1.imshow(corr[dendro['leaves'], :][:, dendro['leaves']])
    ax1.set_xticks(dendro_idx)
    ax1.set_yticks(dendro_idx)
    ax1.set_xticklabels(lables, rotation='vertical')
    ax1.set_yticklabels(lables)
    ims.set_cmap("Blues")

    divider = make_axes_locatable(ax1)
    cax = divider.append_axes("right", size="2%", pad=0.20)

    fig.colorbar(ims, cax=cax)
    fig.tight_layout()

    # plt.show()
    plt.savefig('../Thesis/images/feature_correlation.png')


main()
