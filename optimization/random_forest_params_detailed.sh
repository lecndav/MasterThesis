#!/bin/bash
set -e

data=$1
time=$2
window_size=$3
estimators=$4
max_depth=$5
delete=$6
count=$(find $data/hdf5_* -mindepth 0 -maxdepth 0 -type d | wc -l)
if [[ "$count" -lt 10 ]];
then
  count="0${count}"
fi

dir_name="${data}/hdf5_${count}"
cp -r "${data}/hdf5_xx" $dir_name
echo "created directory ${dir_name}"
echo ""

python3 data_transformation/01_to_hdf5.py -m "${data}/mf4" -o "${dir_name}/stage1" -d $time
python3 data_transformation/02_window_size.py -i "${dir_name}/stage1" -o "${dir_name}/stage2" -s $window_size
python3 data_transformation/03_clean_data.py -i "${dir_name}/stage2" -o "${dir_name}/stage3"
python3 data_transformation/04_add_class_column.py -i "${dir_name}/stage3" -o "${dir_name}/stage4"
echo "Let the magician do his magic."
python optimization/random_forest_params_detailed.py -i "${dir_name}/stage4" -r results/random_forest_params_detailed -e $estimators -d $max_depth

if [[ "$delete" -eq "1" ]];
then
  rm -r ${dir_name}
fi