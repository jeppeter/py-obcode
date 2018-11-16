#! /bin/bash

_script_file=`readlink -f $0`
script_dir=`dirname $_script_file`


rm -f $script_dir/obcode.py.touched
rm -f $script_dir/obcode.py
rm -f $script_dir/src/*.pyc
rm -rf $script_dir/__pycache__
rm -rf $script_dir/src/__pycache__
rm -f $script_dir/obcode.mak
rm -f $script_dir/obmak.py