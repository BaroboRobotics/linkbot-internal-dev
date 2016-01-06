#!/bin/sh

for i in *.ui; do
    pyuic4 $i > `basename $i .ui`.py
done
