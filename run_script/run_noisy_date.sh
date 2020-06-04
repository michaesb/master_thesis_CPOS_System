pytest -v

adress_bjo="../../../data_thesis/share_UiOMichael/Data/20150317/bjo22015076.scn"
adress_bod="../../../data_thesis/share_UiOMichael/Data/20150317/bod22015076.scn"
adress_hon="../../../data_thesis/share_UiOMichael/Data/20150317/hon22015076.scn"
adress_hop="../../../data_thesis/share_UiOMichael/Data/20150317/hop22015076.scn"

adress_kau="../../../data_thesis/share_UiOMichael/Data/20150317/kau22015076.scn"
adress_nya="../../../data_thesis/share_UiOMichael/Data/20150317/nya22015076.scn"
adress_tro="../../../data_thesis/share_UiOMichael/Data/20150317/tro22015076.scn"
adress_veg="../../../data_thesis/share_UiOMichael/Data/20150317/veg22015076.scn"

cd python_plotter
xterm -T "bjorneoya" -geometry 80x24--11+356 -hold -e 'pwd; python single_file_plotter.py ../../../data_thesis/share_UiOMichael/Data/20150317/bjo22015076.scn'&
xterm -T "bod" -geometry 80x24--11+356 -hold -e 'pwd; python single_file_plotter.py ../../../data_thesis/share_UiOMichael/Data/20150317/bod22015076.scn'&
xterm -T "hon" -geometry 80x24--11+356 -hold -e 'pwd; python single_file_plotter.py ../../../data_thesis/share_UiOMichael/Data/20150317/hon22015076.scn'&
xterm -T "hop" -geometry 80x24--11+356 -hold -e 'pwd; python single_file_plotter.py ../../../data_thesis/share_UiOMichael/Data/20150317/hop22015076.scn'&

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

xterm -T "kau" -geometry 80x24--11+356 -hold -e 'pwd; python single_file_plotter.py ../../../data_thesis/share_UiOMichael/Data/20150317/kau22015076.scn'&
xterm -T "nya" -geometry 80x24--11+356 -hold -e 'pwd; python single_file_plotter.py ../../../data_thesis/share_UiOMichael/Data/20150317/nya22015076.scn'&
xterm -T "tro" -geometry 80x24--11+356 -hold -e 'pwd; python single_file_plotter.py ../../../data_thesis/share_UiOMichael/Data/20150317/tro22015076.scn'&
xterm -T "veg" -geometry 80x24--11+356 -hold -e 'pwd; python single_file_plotter.py ../../../data_thesis/share_UiOMichael/Data/20150317/veg22015076.scn'&
