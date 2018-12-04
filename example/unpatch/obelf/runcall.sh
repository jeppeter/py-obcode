#! /bin/bash
cnt=0
TICK=0
maxcnt=1
splitcnt=10
if [ $# -gt 0 ]
	then
	TICK=$1
	shift
fi

if [ $# -gt 0 ]
	then
	maxcnt=$1
	shift
fi

modcnt=`expr $maxcnt \* $splitcnt`
printf "$TICK"
while [ 1 ]
do
	make clean >/dev/null
	curcnt=`expr $cnt % $modcnt`
	make V=1 OB_PATCH=1 CNT=$TICK all 2>&1 | sudo tee /mnt/zdisk/patched_error.${TICK}.${curcnt}.txt >/dev/null
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