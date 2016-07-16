#!/bin/bash
iterations=40
if [ -n "$1" ]; then
  iterations="$1";
fi

for i in `seq 1 ${iterations}`;
do
  mkdir -p $i
  touch $i/$i
done
