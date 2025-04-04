set datafile separator ","
set title "Electron Density in D-Region"
set xlabel "Electron Density (n_e) (m^-3)"
set x2label "Collision Frequency (nu) (s^-1)"
set ylabel "Height (km)"
set grid

# Define styles
set style line 1 lc rgb "blue" lt 1 lw 1 pt 5   # Blue, solid line, thick, square points
set style line 2 lc rgb "red" lt 2 lw 1 pt 7    # Red, dashed line, thick, diamond points

plot "data/test.csv" using 2:1 with linespoints linestyle 1 title "n_e", \
     "data/test.csv" using 3:1 axes x2y1 with linespoints linestyle 2 title "nu"
