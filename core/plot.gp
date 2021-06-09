
reset
set terminal pdfcairo font "Times" square size 21,14 
set output 'graph.pdf'



set xlabel 'time'
set ylabel 'price'


#set xr [900:1000]
set multiplot layout 3,1
plot 'df.csv' u 1:3:5:4:6  w candlesticks notitle,\
     ''       u 1:($14=="1d"?$4:1/0) w points pt 8 ps 1 lc "green",\
     ''       u 1:($14=="2c"?$4:1/0) w points pt 3 ps 1 lc "red",\

plot 'df.csv' u 1:13  w impulses lc 'blue' notitle "SMI"
plot 'df.csv' u 1:12  w lines lc 'black' notitle "ADX"






unset multiplot 
