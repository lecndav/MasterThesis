#!/bin/bash
set -e

time=$1
window_size=$2
delete=$3
count=$(find data/hdf5_* -mindepth 0 -maxdepth 0 -type d | wc -l)
if [[ "$count" -lt 10 ]];
then
  count="0${count}"
fi

dir_name="data/hdf5_${count}"
cp -r data/hdf5_xx $dir_name
echo "created directory ${dir_name}"
echo ""

python3 data_transformation/01_to_hdf5.py -m data/mf4 -o "${dir_name}/stage1" -d $time 1> "${dir_name}/stage1/out.std" 2> "${dir_name}/stage1/out.err"
python3 data_transformation/02_window_size.py -i "${dir_name}/stage1" -o "${dir_name}/stage2" -s $window_size 1> "${dir_name}/stage2/out.std" 2> "${dir_name}/stage2/out.err"
python3 data_transformation/03_remove_0_speed.py -i "${dir_name}/stage2" -o "${dir_name}/stage3" 1> "${dir_name}/stage3/out.std" 2> "${dir_name}/stage3/out.err"
python3 data_transformation/04_add_class_column.py -i "${dir_name}/stage3" -o "${dir_name}/stage4" 1> "${dir_name}/stage4/out.std" 2> "${dir_name}/stage4/out.err"
echo "Let the magician do his work."
python magic/magic.py -i "${dir_name}/stage4"

if [[ "$delete" -eq "1" ]];
then
  rm -r ${dir_name}
fi