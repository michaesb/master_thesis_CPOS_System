#!/bin/bash
pytest -v
#not in use

cd python_plotter
xterm -T "bjo" -geometry 80x24+0+1 -hold -e 'python single_RTIMfile_plotter.py ../../../data_thesis/data/RTIM/2015/03/17/Scintillation/bjo22015076.scn'&
sleep 0.1

#getting the program to wait until you press c
echo "Press c to continue"
count=0
while : ; do
read -n 1 k <&1
if [[ $k = c ]] ; then
printf "\n continuing \n"
break
else
((count=$count+1))
printf "\try again \n"
echo "Press c to continue"
fi
done
