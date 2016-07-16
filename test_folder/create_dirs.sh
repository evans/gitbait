#!/bin/bash
for i in `seq 1 9`;
do
  mkdir -p $i
  touch $i/$i
done
