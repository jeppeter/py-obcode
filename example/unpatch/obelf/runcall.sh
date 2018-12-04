#! /bin/bash
cnt=0
TICK=0
if [ $# -gt 0 ]
	then
	TICK=$1
fi

printf "$TICK"
while [ 1 ]
do
	make clean >/dev/null
	curcnt=`expr $cnt % 10`
	make V=1 OB_PATCH=1 CNT=$TICK all 2>&1 | sudo tee /mnt/zdisk/patched_error.${TICK}.${curcnt}.txt >/dev/null
	_res=$?
	if [ $_res -ne 0 ]
		then
		break
	fi
	printf .
	cnt=`expr $cnt + 1`
	modnum=`expr $cnt \% 10`
	if [ $modnum -eq 0 ]
		then
		printf "\n"
		TICK=`expr $TICK + 1`
		printf "$TICK"
	fi
done