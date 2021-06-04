
reset
set terminal pdfcairo font "Times" square size 21,7 
set output 'graph.pdf'



set xlabel 'time'
set ylabel 'price'


set xr [800:1000]
set multiplot layout 3,1
plot 'df.csv' u 1:3:5:4:6  w candlesticks notitle

plot 'df.csv' u 1:13  w impulses lc 'blue' notitle




unset multiplot 
