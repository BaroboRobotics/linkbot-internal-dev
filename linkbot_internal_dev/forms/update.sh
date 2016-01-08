#!/bin/sh

for i in *.ui; do
    pyuic4 $i > `basename $i .ui`.py
done

for i in *.qrc; do
    pyrcc4 -py3 -o `basename $i .qrc`_rc.py $i
done
