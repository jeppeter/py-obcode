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
rm -f $script_dir/obmak.py.touched 
rm -f $script_dir/obmak.py
rm -f $script_dir/obpatch.py.touched 
rm -f $script_dir/obpatch.py
rm -f $script_dir/src/chkval.py

$PYTHON -m insertcode -p '%C_CODE_CRC32CALC%' -i $script_dir/src/chkval.py.tmpl pythonc $script_dir/src/crc32calc.c | \
$PYTHON -m insertcode -p '%C_CODE_MD5CALC%' pythonc $script_dir/src/md5calc.c | \
$PYTHON -m insertcode -p '%C_CODE_SHA256CALC%' pythonc $script_dir/src/sha256calc.c | \
$PYTHON -m insertcode -p '%C_CODE_SHA3CALC%' pythonc $script_dir/src/sha3calc.c | \
$PYTHON -m insertcode -p '%C_CODE_CHKVALDEF%' pythonc $script_dir/src/chkvaldef.c | \
$PYTHON -m insertcode -p '%C_CODE_CHKVAL%' -o $script_dir/src/chkval.py pythonc $script_dir/src/chkval.c

$PYTHON $script_dir/src/obcode_debug.py --release
wait_file_until "$script_dir/obcode.py.touched"
$PYTHON $script_dir/src/obmak_debug.py --release
wait_file_until "$script_dir/obmak.py.touched"
$PYTHON $script_dir/src/obpatch_debug.py --release
wait_file_until "$script_dir/obpatch.py.touched"

$PYTHON -m insertcode -p '%OBMAK_CODE%' -i $script_dir/src/obcode.mak.tmpl bz2base64mak  $script_dir/obmak.py | $PYTHON -m insertcode -p '%OBPATCH_CODE%' -o $script_dir/obcode.mak bz2base64mak $script_dir/obpatch.py

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
