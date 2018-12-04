#! /bin/bash

_script_file=`readlink -f $0`
_script_dir=`dirname $_script_file`

function dump_file()
{
	_src=$1
	_outbase=$2
	objdump -D "$_src" | sudo tee /mnt/zdisk/${_outbase}.objdump.txt >/dev/null
	readelf -a "$_src" | sudo tee /mnt/zdisk/${_outbase}.readelf.txt >/dev/null
}

dumpname="nopatch"
if [ $# -gt 0 ]
	then
	dumpname="patched"
fi


dump_file "$_script_dir/callc.o" "callc.o.${dumpname}"
dump_file "$_script_dir/main.o" "main.o.${dumpname}"
dump_file "$_script_dir/main2.o" "main2.o.${dumpname}"
dump_file "$_script_dir/main" "main.${dumpname}"
dump_file "$_script_dir/main2" "main2.${dumpname}"