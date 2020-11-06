#!/usr/bin/env bash

# gdal_calc.py must be in the path for this script to work.

cd $(dirname "$0")

mkdir -p ../geoserver/data/store

for year in {2019..2019}; do
  for month in {04..10}; do
    month_formatted=$(printf "%02d" $month)
    gdal_calc.py \
        -A "./inputs/$year.$month_formatted.15.nir.tif" \
        -B "./inputs/$year.$month_formatted.15.green.tif" \
        --calc "(A/B)-1" \
        --type Float32 \
        --outfile "../geoserver/data/store/$year.$month_formatted.15.gcvi.tif"
  done
done
