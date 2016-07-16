#!/bin/bash
iterations=40
if [ -n "$1" ]; then
  iterations="$1";
fi

for i in `seq -f "%05g" 1 ${iterations}`;
do
  rm -r $i
done
