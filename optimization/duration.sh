#!/bin/bash
set -e

data=$1
window_size=$2
count=$(find $data/hdf5_* -mindepth 0 -maxdepth 0 -type d | wc -l)
if [[ "$count" -lt 10 ]];
then
  count="0${count}"
fi

dir_name="${data}/hdf5_${count}"
cp -r "${data}/hdf5_xx" $dir_name
echo "created directory ${dir_name}"
echo ""

python3 data_transformation/01_to_hdf5.py -m "${data}/mf4" -o "${dir_name}/stage1" -d 35
python3 data_transformation/02_window_size.py -i "${dir_name}/stage1" -o "${dir_name}/stage2" -s $window_size
python3 data_transformation/03_clean_data.py -i "${dir_name}/stage2" -o "${dir_name}/stage3"
python3 data_transformation/04_add_class_column.py -i "${dir_name}/stage3" -o "${dir_name}/stage4"
echo "Let the magician do his magic."
python optimization/duration.py -i "${dir_name}/stage4"  -r results  -s $window_size

rm -r ${dir_name}