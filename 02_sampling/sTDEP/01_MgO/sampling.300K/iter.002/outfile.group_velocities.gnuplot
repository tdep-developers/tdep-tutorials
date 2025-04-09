 set terminal qt  size 500,350 enhanced font "CMU Serif,10"
 unset xtics
 set xtics ( "Γ" 0.0 ) 
set xtics add ("X"  0.125227  )
set xtics add ("U|K"  0.169501  )
set xtics add ("Γ"  0.302324  )
set xtics add ("L"  0.410773  )
 set grid xtics lc rgb "#888888" lw 1 lt 0
 set xzeroaxis linewidth 0.1 linecolor 0 linetype 1
 set ytics scale 0.5
 set xtics scale 0.5
 set mytics 10
 unset key
 set ylabel "Group velocity (km/s)"
plot "outfile.group_velocities" u 1:2 w line lc rgb "#618712",\
 "outfile.group_velocities" u 1:3 w line lc rgb "#618712",\
 "outfile.group_velocities" u 1:4 w line lc rgb "#618712",\
 "outfile.group_velocities" u 1:5 w line lc rgb "#618712",\
 "outfile.group_velocities" u 1:6 w line lc rgb "#618712",\
 "outfile.group_velocities" u 1:7 w line lc rgb "#618712"
