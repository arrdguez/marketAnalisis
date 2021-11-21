reset
set terminal pdfcairo size 14,10
set output 'graph.pdf'

set style histogram cluster gap 1
set style fill solid
set style line 1 lc rgb "red"
set style line 2 lc rgb "blue"
set style line 2 lc rgb "red"
set style line 3 lc rgb "blue"
set style line 4 lc rgb "red"
set style line 5 lc rgb "blue"
set style line 6 lc rgb "red"
set style line 7 lc rgb "blue"
set style line 8 lc rgb "red"
set style line 9 lc rgb "blue"


set multiplot layout 3,2
p '5000_sorted.dat' index 0 every 1 u 0:5:6:xticlabels(3) w boxes lc variable  t 'BTCUSDT 3m'
p '5000_sorted.dat' index 1 every 1 u 0:5:6:xticlabels(3) w boxes lc variable  t 'BTCUSDT 5m'
p '5000_sorted.dat' index 2 every 1 u 0:5:6:xticlabels(3) w boxes lc variable  t 'BTCUSDT 15m'
p '5000_sorted.dat' index 3 every 1 u 0:5:6:xticlabels(3) w boxes lc variable  t 'BTCUSDT 30m'
p '5000_sorted.dat' index 4 every 1 u 0:5:6:xticlabels(3) w boxes lc variable  t 'BTCUSDT 1h'
p '5000_sorted.dat' index 5 every 1 u 0:5:6:xticlabels(3) w boxes lc variable  t 'BTCUSDT 4h'
unset multiplot

set multiplot layout 3,2
p '5000_sorted.dat' index 6 every 1 u 0:5:6:xticlabels(3) w boxes lc variable  t 'ETHUSDT 3m'
p '5000_sorted.dat' index 7 every 1 u 0:5:6:xticlabels(3) w boxes lc variable  t 'ETHUSDT 5m'
p '5000_sorted.dat' index 8 every 1 u 0:5:6:xticlabels(3) w boxes lc variable  t 'ETHUSDT 15m'
p '5000_sorted.dat' index 9 every 1 u 0:5:6:xticlabels(3) w boxes lc variable  t 'ETHUSDT 30m'
p '5000_sorted.dat' index 10 every 1 u 0:5:6:xticlabels(3) w boxes lc variable  t 'ETHUSDT 1h'
p '5000_sorted.dat' index 11 every 1 u 0:5:6:xticlabels(3) w boxes lc variable  t 'ETHUSDT 4h'
unset multiplot

set multiplot layout 3,2
p '5000_sorted.dat' index 12 every 1 u 0:5:6:xticlabels(3) w boxes lc variable  t 'BNBUSDT 3m'
p '5000_sorted.dat' index 13 every 1 u 0:5:6:xticlabels(3) w boxes lc variable  t 'BNBUSDT 5m'
p '5000_sorted.dat' index 14 every 1 u 0:5:6:xticlabels(3) w boxes lc variable  t 'BNBUSDT 15m'
p '5000_sorted.dat' index 15 every 1 u 0:5:6:xticlabels(3) w boxes lc variable  t 'BNBUSDT 30m'
p '5000_sorted.dat' index 16 every 1 u 0:5:6:xticlabels(3) w boxes lc variable  t 'BNBUSDT 1h'
p '5000_sorted.dat' index 17 every 1 u 0:5:6:xticlabels(3) w boxes lc variable  t 'BNBUSDT 4h'
unset multiplot
set multiplot layout 3,2
p '5000_sorted.dat' index 18 every 1 u 0:5:6:xticlabels(3) w boxes lc variable  t 'ADAUSDT 3m'
p '5000_sorted.dat' index 19 every 1 u 0:5:6:xticlabels(3) w boxes lc variable  t 'ADAUSDT 5m'
p '5000_sorted.dat' index 20 every 1 u 0:5:6:xticlabels(3) w boxes lc variable  t 'ADAUSDT 15m'
p '5000_sorted.dat' index 21 every 1 u 0:5:6:xticlabels(3) w boxes lc variable  t 'ADAUSDT 30m'
p '5000_sorted.dat' index 22 every 1 u 0:5:6:xticlabels(3) w boxes lc variable  t 'ADAUSDT 1h'
p '5000_sorted.dat' index 23 every 1 u 0:5:6:xticlabels(3) w boxes lc variable  t 'ADAUSDT 4h'
unset multiplot