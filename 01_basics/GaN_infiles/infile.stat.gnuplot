dir=system("pwd")
set terminal aqua size 1200,800 font "CMU Serif,10"
#Uncomment the following two lines to save a png file of the plot
#set terminal pngcairo size 1200,800 font ",12"
#set out "statplot.png"
set fit logfile system("mktemp")
set multiplot
 set border lw 0.5 
 set ytics scale 0.5 
 set xtics scale 0.5 
 set mxtics 5 
 set mytics 5 
  
 set style line 1 lc rgb "#65CAAE" lw 1 
 set style line 2 lc rgb "#CC8F12" lw 1 
 set style line 3 lc rgb "#88172B" lw 1 
 set style line 4 lc rgb "#90AB3F" lw 1 
 set style line 5 lc rgb "#FDF488" lw 1 
 set style line 6 lc rgb "#528E7C" lw 1 
 set style increment user 
set title font "CMU Serif,14"
set xlabel "Time (ps)"
set size 1.0,1.0
f2p(n) = real(n)/1000.0
set origin 0.0, 0.0
set size 0.5, 0.5
set title "Total Energy"
set ylabel "Energy (eV)"
fe(x) = ae *x + be
fit fe(x) "infile.stat" u (f2p($2)):3 via ae, be
plot "infile.stat" u (f2p($2)):3 t "Energy" w line, \
fe(x) t sprintf("fit: %f*t + %f", ae,be)
set origin 0.0, 0.5
set size 0.5, 0.5
set title "Temperature"
set ylabel "Temperature (K)"
ft(x) = at *x + bt
fit ft(x) "infile.stat" u (f2p($2)):6 via at, bt
plot "infile.stat" u (f2p($2)):6 t "Temperature" w line, \
ft(x) t sprintf("fit: %f*t + %f", at,bt)
set origin 0.5, 0.0
set size 0.5, 0.5
set title "Pressure"
set ylabel "Pressure (GPa)"
fp(x) = ap *x + bp
fit fp(x) "infile.stat" u (f2p($2)):7 via ap, bp
plot "infile.stat" u (f2p($2)):7 t "Pressure" w line,\
fp(x) t sprintf("fit: %f*t + %f", ap,bp)
set origin 0.5, 0.5
set size 0.5, 0.5
set title "Stress"
set ylabel "Stress (GPa)"
plot "infile.stat" u (f2p($2)):8 t "x" w line,\
"infile.stat" u (f2p($2)):9  t "y"  w line,\
"infile.stat" u (f2p($2)):10 t "z"  w line,\
"infile.stat" u (f2p($2)):11 t "xy" w line,\
"infile.stat" u (f2p($2)):12 t "zy" w line,\
"infile.stat" u (f2p($2)):13 t "zx" w line
unset multiplot
