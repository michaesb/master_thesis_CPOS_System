#!/bin/bash
pytest -v


cd python_plotter
xterm -T "bod" -geometry 80x24+0+1 -hold -e 'python single_RTIMfile_plotter.py ../../../data_thesis/data/RTIM/2015/06/23/Scintillation/bod22015174.scn'&
sleep 0.1
xterm -T "far" -geometry 80x24+450+1 -hold -e 'python single_RTIMfile_plotter.py ../../../data_thesis/data/RTIM/2015/06/23/Scintillation/far22015174.scn'&
sleep 0.1
xterm -T "hon" -geometry 80x24+900+1 -hold -e 'python single_RTIMfile_plotter.py ../../../data_thesis/data/RTIM/2015/06/23/Scintillation/hon22015174.scn'&
sleep 0.1
xterm -T "hof" -geometry 80x24+1350+1 -hold -e 'python single_RTIMfile_plotter.py ../../../data_thesis/data/RTIM/2015/06/23/Scintillation/hof22015174.scn'&
#getting the program to wait until you press c
echo "Press c to continue"

while : ; do
read -n 1 k <&1
if [[ $k = c ]] ; then
printf "\n continuing \n"
break
fi
done



xterm -T "hop" -geometry 80x24+0+200 -hold -e 'python single_RTIMfile_plotter.py ../../../data_thesis/data/RTIM/2015/06/23/Scintillation/hop22015174.scn'&
sleep 0.1
xterm -T "kau" -geometry 80x24+450+200 -hold -e 'python single_RTIMfile_plotter.py ../../../data_thesis/data/RTIM/2015/06/23/Scintillation/kau22015174.scn'&
sleep 0.1
xterm -T "veg" -geometry 80x24+900+200 -hold -e 'python single_RTIMfile_plotter.py ../../../data_thesis/data/RTIM/2015/06/23/Scintillation/veg22015174.scn'&
sleep 0.1
xterm -T "nya" -geometry 80x24+1350+200 -hold -e 'python single_RTIMfile_plotter.py ../../../data_thesis/data/RTIM/2015/06/23/Scintillation/nya22015174.scn'&


#getting the program to wait until you press c
echo "Press c to continue"
while : ; do
read -n 1 k <&1
if [[ $k = c ]] ; then
printf "\n continuing \n"
break

fi
done


xterm -T "tro" -geometry 80x24+0+400 -hold -e 'python single_RTIMfile_plotter.py ../../../data_thesis/data/RTIM/2015/06/23/Scintillation/tro22015174.scn'&
