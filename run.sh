#!/bin/bash
declare -a tags=( #"volunteer" 
				  #"donate"
				  "elderlycare"
				  "healthcare"
				  "disability"

				  #"eco"
				  "climatechange"
				  "environment"
				  #"hunger" 
				  #"education"
				  "charity"
				  "socialgood"

				  "endangered"
				  "endangeredspecies")


if [ ! -d data ] 
then
    mkdir -p data
    mkdir -p data/process
fi 


# Length of the array
length=${#tags[@]}

# Array Loop
for (( i=0; i < ${length}; i++ ))
do
  Rscript jsonReader.R ${tags[$i]}
  # python  data_preprocess.py ${tags[$i]}
done

