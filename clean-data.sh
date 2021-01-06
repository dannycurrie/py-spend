#!/bin/bash

awk -F'"' -v OFS='' '{ for (i=2; i<=NF; i+=2) gsub(",", "", $i) } 1' ./put-data-here/data.csv > ./put-data-here/data-cleaned.csv 