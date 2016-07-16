#!/bin/bash
for i in `seq 1 40`;
do
  mkdir -p test_folder/$i
  touch test_folder/$i/$i
done
