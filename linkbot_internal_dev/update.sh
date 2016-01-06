#!/bin/sh

pyuic4 mainwindow.ui > mainwindow.py

cd forms
./update.sh
