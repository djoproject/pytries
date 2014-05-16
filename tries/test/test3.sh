#!/bin/bash

#export PYTHONPATH=/home/jdv/development/tries_shell/pytries:$PYTHONPATH
export PYTHONPATH=$(pwd)/../../:$PYTHONPATH
echo $PYTHONPATH
python3 tries_testunit.py || exit
python3 insert_test.py || exit
python3 mt_testunit.py || exit
python3 remove_test.py || exit
python3 search_test.py || exit
python3 traversal_test.py || exit
