#!/bin/bash

#create arborescence
mkdir pytries_install
mkdir pytries_install/tries

#copy files
cp ./setup.py ./pytries_install/.
cp ./README.md ./pytries_install/.
cp ./example.py ./pytries_install/.

cp ./tries/__init__.py ./pytries_install/tries/.
cp ./tries/exception.py ./pytries_install/tries/.
cp ./tries/multiLevelTries.py ./pytries_install/tries/.
#cp ./tries/suffixTries.py ./pytries_install/tries/.
cp ./tries/utils.py ./pytries_install/tries/.
cp ./tries/tries.py ./pytries_install/tries/.

#zip the directory
zip -r pytries_v1.0.zip ./pytries_install/

rm -r ./pytries_install/