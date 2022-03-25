#!/bin/bash
# repo https://github.com/raspiuser1/Automate-Wolfgarten-S150-wif


#only active between month 4 and 10, you can remove this or edit it
maandnu=$(date +%m)
if [ $maandnu -lt "3" ] || [ $maandnu -gt "10" ]
then
	echo "Exit: er word alleen Gemaaid in de maand 4 tm 10"
	exit 1
fi


if [ "$1" = "" ]; then
echo "Exit: Geef een argument/optie" 
exit 1
fi

if [ $1 = "noodstop.home" ]
then
    postdata="2222"
fi
if [ $1 = "grasmaaier.uit" ]
then
    postdata="3333"
fi


if [ $1 = "normale.maaibeurt" ]
then
    postdata="7777"
fi


if [ $1 = "korte.maaibeurt" ]
then
    postdata="1111"
fi

if [ $1 = "kinderslot.aan" ]
then
    postdata="4444"
fi
if [ $1 = "kinderslot.uit" ]
then
    postdata="6666"
fi

if [ $1 = "maaien.met.kinderslot" ]
then
    postdata="5555"
fi

timing="timings=$postdata"
echo $timing

/usr/bin/curl -X POST -H "Content-Type: application/x-www-form-urlencoded; charset=utf-8" --data-ascii $timing http://192.168.1.122/play
