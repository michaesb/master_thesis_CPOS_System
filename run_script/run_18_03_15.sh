#!/bin/bash
pytest -v

bod22015174.scn  far22015174.scn  hof22015174.scn  hon22015174.scn  hop22015174.scn  kau22015174.scn  nya22015174.scn  tro22015174.scn  veg22015174.scn

#/home/michaelsb/data_thesis/data/RTIM/2015/03/18/Scintillation

cd python_plotter
xterm -T "bjo" -geometry 80x24+0+1 -hold -e 'python single_file_plotter.py ../../../data_thesis/data/RTIM/2015/03/18/Scintillation/bjo22015077.scn'&
sleep 0.1
xterm -T "bod" -geometry 80x24+450+1 -hold -e 'python single_file_plotter.py ../../../data_thesis/data/RTIM/2015/03/18/Scintillation/bod22015077.scn'&
sleep 0.1
xterm -T "far" -geometry 80x24+900+1 -hold -e 'python single_file_plotter.py ../../../data_thesis/data/RTIM/2015/03/18/Scintillation/far22015077.scn'&
sleep 0.1
xterm -T "hon" -geometry 80x24+1350+1 -hold -e 'python single_file_plotter.py ../../../data_thesis/data/RTIM/2015/03/18/Scintillation/hon22015077.scn'&

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

xterm -T "hop" -geometry 80x24+0+200 -hold -e 'python single_file_plotter.py ../../../data_thesis/data/RTIM/2015/03/18/Scintillation/hop22015077.scn'&
sleep 0.1
xterm -T "jan" -geometry 80x24+450+200 -hold -e 'python single_file_plotter.py ../../../data_thesis/data/RTIM/2015/03/18/Scintillation/jan22015077.scn'&
sleep 0.1
xterm -T "kau" -geometry 80x24+900+200 -hold -e 'python single_file_plotter.py ../../../data_thesis/data/RTIM/2015/03/18/Scintillation/kau22015077.scn'&
sleep 0.1
xterm -T "veg" -geometry 80x24+1350+200 -hold -e 'python single_file_plotter.py ../../../data_thesis/data/RTIM/2015/03/18/Scintillation/veg22015077.scn'&


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


xterm -T "tro" -geometry 80x24+900+400 -hold -e 'python single_file_plotter.py ../../../data_thesis/data/RTIM/2015/03/18/Scintillation/tro22015077.scn'&
sleep 0.1
xterm -T "nya" -geometry 80x24+1350+400 -hold -e 'python single_file_plotter.py ../../../data_thesis/data/RTIM/2015/03/18/Scintillation/nya22015077.scn'&
