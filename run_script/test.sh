#!/bin/bash
echo "Press c to continue"
count=0
while : ; do
read -n 1 k <&1
if [[ $k = c ]] ; then
printf "\n continuing \n"
break
else
((count=$count+1))
printf "\nIterate for $count times\n"
echo "Press c to continue"
fi
done
