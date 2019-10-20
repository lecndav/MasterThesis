import argparse
import pathlib
import os
import sys
from asammdf import MDF, Signal
import numpy as np


interesting_signals = ['can0_LWI_Lenkradwinkel', 'can0_ESP_Fahrer_bremst', 'can0_ESP_Bremsdruck',
                       'can0_MO_Drehzahl_01', 'can0_MO_Gangposition', 'can0_ESP_v_Signal',  'can0_ESP_HL_Fahrtrichtung', 'can0_ESP_HR_Fahrtrichtung', 'can0_LWI_Lenkradw_Geschw', 'can0_ESP_Querbeschleunigung', 'can0_ESP_Laengsbeschl', 'can0_ESP_Gierrate', 'can0_MO_Fahrpedalrohwert_01', 'can0_MO_Kuppl_schalter']

def main():

  my_parser = argparse.ArgumentParser(description='Transform signals with sign')
  my_parser.add_argument('-i', '--input',
                         action='store',
                         metavar='mf4_input',
                         type=str,
                         required=True,
                         help='Input directory with source mf4 files')

  my_parser.add_argument('-o', '--output',
                         action='store',
                         metavar='mf4_output',
                         type=str,
                         required=True,
                         help='Output directory')

  # Execute the parse_args() method
  args = my_parser.parse_args()

  mf4_input = args.input
  mf4_output = args.output

  if not os.path.isdir(mf4_input):
    print('The mf4 input path specified is not a directory')
    sys.exit()

  if not os.path.isdir(mf4_output):
    print('The mf4 ouput path specified is not a directory')
    sys.exit()

  for file in os.listdir(mf4_input):
    if not file.endswith('.mf4'):
      continue
    print('process %s' % file)
    mdf_file = MDF(os.path.join(mf4_input, file))

    # Lenkradwinkel
    lenkradwinkel = mdf_file.get('can0_LWI_Lenkradwinkel')
    samples = list(lenkradwinkel.samples)
    vz_samples = list(mdf_file.get('can0_LWI_VZ_Lenkradwinkel').samples)
    for i in range(0, len(samples)):
      if not int(vz_samples[i]):
        samples[i] = samples[i] * -1
    lenkradwinkel.samples = np.asarray(samples)

    # Lenkradwinkel geschw.
    lenkradwinkel = mdf_file.get('can0_LWI_Lenkradw_Geschw')
    samples = list(lenkradwinkel.samples)
    vz_samples = list(mdf_file.get('can0_LWI_VZ_Lenkradw_Geschw').samples)
    for i in range(0, len(samples)):
      if not int(vz_samples[i]):
        samples[i] = samples[i] * -1
    lenkradwinkel.samples = np.asarray(samples)

    # Gierrate
    lenkradwinkel = mdf_file.get('can0_ESP_Gierrate')
    samples = list(lenkradwinkel.samples)
    vz_samples = list(mdf_file.get('can0_ESP_VZ_Gierrate').samples)
    for i in range(0, len(samples)):
      if not int(vz_samples[i]):
        samples[i] = samples[i] * -1
    lenkradwinkel.samples = np.asarray(samples)

    # filter file with VZ signals
    filtered_mdf = mdf_file.filter(interesting_signals)
    filtered_mdf.save(os.path.join(mf4_output, file))
    
    break

main()
