 set terminal aqua size 500,350 enhanced font "CMU Serif,10"
 unset xtics
 set xtics ( "Γ" 0.0 ) 
set xtics add ("H"  0.146994  )
set xtics add ("N"  0.250934  )
set xtics add ("Γ"  0.354874  )
set xtics add ("P"  0.482174  )
set xtics add ("H"  0.609475  )
 set grid xtics lc rgb "#888888" lw 1 lt 0
 set xzeroaxis linewidth 0.1 linecolor 0 linetype 1
 set ytics scale 0.5
 set xtics scale 0.5
 set mytics 10
 unset key
 set ylabel "Frequency (THz)"
plot "outfile.dispersion_relations" u 1:2 w line lc rgb "#618712",\
 "outfile.dispersion_relations" u 1:3 w line lc rgb "#618712",\
 "outfile.dispersion_relations" u 1:4 w line lc rgb "#618712"
