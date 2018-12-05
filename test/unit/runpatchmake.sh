#! /bin/bash

_isok=`which extargsparse4sh`
if [ -z "$_isok" ]
	then
	/bin/echo "please setup extargsparse4sh from https://github.com/jeppeter/extargsparse4sh.git" >&2
	exit 4
fi

source extargsparse4sh

read -r -d ''  OPTIONS<<EOFMM
    {
    	"verbose|v" : "+",
        "tick|T" : 0,
        "maxcnt|M" : 1,
        "splitcnt|S" : 10,
        "outdir|D" : "/mnt/zdisk",
        "\$<args>" : 1
    }
EOFMM


parse_command_line "$OPTIONS" "$@"



cnt=0
TICK=$tick
if [ $maxcnt -eq 0 ]
	then
	/bin/echo "not 0 allowed" >&2
	exit 4
fi

rundir=${args[0]}
modcnt=`expr $maxcnt \* $splitcnt`
if [ $verbose -ge 3 ]
	then
	_printout=
else
	_printout=--no-print-directory
fi
printf "$TICK"
while [ 1 ]
do
	make -C $rundir $_printout clean >/dev/null
	curcnt=`expr $cnt % $modcnt`
	make -C $rundir $_printout V=1 OB_PATCH=1 CNT=$TICK all >$outdir/patched_error.${TICK}.${curcnt}.txt 2>&1
	_res=$?
	if [ $_res -ne 0 ]
		then
		break
	fi
	printf .
	cnt=`expr $cnt + 1`
	modnum=`expr $cnt \% $splitcnt`
	if [ $modnum -eq 0 ]
		then
		printf "\n"
		if [ $cnt -ge $modcnt ]
			then
			TICK=`expr $TICK + 1`
			cnt=0
		fi
		printf "$TICK"
	fi
done