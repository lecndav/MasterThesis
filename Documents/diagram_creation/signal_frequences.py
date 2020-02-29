import sys
import math
import os
import numpy as np
import matplotlib.pylab as plt
from asammdf import MDF
from random import randint

def main():
    file = sys.argv[1]
    mdf_file = MDF(file)
    mdf_file = mdf_file.filter([
        'can0_LWI_Lenkradwinkel', 'can0_LWI_Lenkradw_Geschw',
        'can0_ESP_Fahrer_bremst', 'can0_ESP_Bremsdruck',
        'can0_MO_Fahrpedalrohwert_01', 'can0_MO_Kuppl_schalter',
        'can0_MO_Drehzahl_01', 'can0_MO_Gangposition', 'can0_ESP_v_Signal',
        'can0_ESP_HL_Fahrtrichtung', 'can0_ESP_HR_Fahrtrichtung',
        'can0_ESP_Laengsbeschl', 'can0_ESP_Gierrate'
    ])
    signals = mdf_file.iter_channels(skip_master=True)
    sf = dict()
    for signal in signals:
        f = len(signal.timestamps) / (signal.timestamps[-1] - signal.timestamps[0])
        sf[signal.name[5:]] = f

    values = list(map(lambda x: int(math.ceil(x)/10) * 10, sf.values()))
    signal_names = list(map(lambda x: '_'.join(x.split('_')[1:]), sf.keys()))
    fig, ax = plt.subplots(figsize=[8,4])
    plt.bar(range(len(sf)), values, align='center')
    plt.yticks(np.arange(0, max(values)+10, 10))
    plt.ylabel('Frequency [Hz]')
    plt.xticks(range(len(sf)), signal_names, rotation='vertical')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(color='gray', linestyle='-', linewidth=0.25, alpha=0.5)

    plt.savefig('../Thesis/images/signal_frequences.png', bbox_inches='tight')
    # plt.show()

main()
