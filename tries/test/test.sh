#!/bin/bash

#export PYTHONPATH=/home/jdv/development/tries_shell/pytries:$PYTHONPATH
export PYTHONPATH=$(pwd)/../../:$PYTHONPATH
echo $PYTHONPATH
python tries_testunit.py || exit
python insert_test.py || exit
python mt_testunit.py || exit
python remove_test.py || exit
python search_test.py || exit
python traversal_test.py || exit
