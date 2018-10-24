#! /bin/bash

_script_file=`readlink -f $0`
script_dir=`dirname $_script_file`

if [ -z "$PYTHON" ]
	then
	PYTHON=python
	export PYTHON
fi
echo "PYTHON [$PYTHON]" >&2

wait_file_until()
{
	_waitf="$1"
	_maxtime=100
	_checked=0
	if [ $# -gt 1 ]
		then
		_maxtime=$2
	fi
	_cnt=0
	while [ 1 ]
	do
		if [ -f "$_waitf" ]
			then
			if [ $_checked -gt 3 ]
				then
				rm -f "$_waitf"
				break
			fi
			/bin/echo -e "import time\ntime.sleep(0.1)" | $PYTHON
			_checked=`expr $_checked \+ 1`
		else
			_checked=0
			/bin/echo -e "import time\ntime.sleep(0.1)" | $PYTHON	
			_cnt=`expr $_cnt \+ 1`
			if [ $_cnt -gt $_maxtime ]
				then
				/bin/echo "can not wait ($_waitf)" >&2
				exit 3
			fi
		fi
	done	
}

rm -f $script_dir/obcode.py.touched 
rm -f $script_dir/obcode.py

$PYTHON $script_dir/src/obcode_debug.py --release
wait_file_until "$script_dir/obcode.py.touched"
$PYTHON -m insertcode -p '%PYTHON_OBCODE_STR%' -i $script_dir/src/obcode.mak.tmpl -o $script_dir/obcode.mak makepython $script_dir/obcode.py

if [ $? -ne 0 ]
	then
	echo "not insert code error" >&2
	exit 4
fi

$PYTHON $script_dir/test/unit/test.py -f
if [ $? -ne 0 ]
	then
	echo "not test ok" >&2
	exit 4
fi
