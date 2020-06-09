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
xterm -T "bjo" -geometry 80x24+0+1 -hold -e 'python single_file_plotter.py plot ../../../data_thesis/share_UiOMichael/Data/20150317/bjo22015076.scn'&
sleep 0.1
xterm -T "bod" -geometry 80x24+450+1 -hold -e 'python single_file_plotter.py plot ../../../data_thesis/share_UiOMichael/Data/20150317/bod22015076.scn'&
sleep 0.1
xterm -T "hon" -geometry 80x24+900+1 -hold -e 'python single_file_plotter.py plot ../../../data_thesis/share_UiOMichael/Data/20150317/hon22015076.scn'&
sleep 0.1
xterm -T "hop" -geometry 80x24+1350+1 -hold -e 'python single_file_plotter.py plot ../../../data_thesis/share_UiOMichael/Data/20150317/hop22015076.scn'&

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

xterm -T "kau" -geometry 80x24+0+200 -hold -e 'python single_file_plotter.py plot ../../../data_thesis/share_UiOMichael/Data/20150317/kau22015076.scn'&
sleep 0.1
xterm -T "nya" -geometry 80x24+450+200 -hold -e 'python single_file_plotter.py plot ../../../data_thesis/share_UiOMichael/Data/20150317/nya22015076.scn'&
sleep 0.1
xterm -T "tro" -geometry 80x24+900+200 -hold -e 'python single_file_plotter.py plot ../../../data_thesis/share_UiOMichael/Data/20150317/tro22015076.scn'&
sleep 0.1
xterm -T "veg" -geometry 80x24+1350+200 -hold -e 'python single_file_plotter.py plot ../../../data_thesis/share_UiOMichael/Data/20150317/veg22015076.scn'&
