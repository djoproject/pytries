#!/bin/bash

#export PYTHONPATH=/home/jdv/development/tries_shell/pytries:$PYTHONPATH
export PYTHONPATH=$(pwd)/../../:$PYTHONPATH
echo $PYTHONPATH
python tries_testunit.py
python insert_test.py
python mt_testunit.py
python remove_test.py
python search_test.py
python traversal_test.py
