#!/bin/sh

# Move the data where the tool expects to find the excel file
mkdir data
mv *.xlsx data

# Run n recom tool with script parameters
python main.py --output json "$@"
