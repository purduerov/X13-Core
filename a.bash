#!/usr/bin/env bash

#move into images folder for use

delete=yes
for file in *.jpg
do
    if [ $delete = yes ]
    then rm -f $file; delete=no
    else delete=yes
    fi
done