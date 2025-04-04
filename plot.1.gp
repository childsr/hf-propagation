set datafile separator ","
set title "integrand"
set xlabel "n_e * nu (m^-3 * s^-1)"
set ylabel "Height (km)"
set grid

# Define styles
set style line 1 lc rgb "blue" lt 1 lw 1 pt 5   # Blue, solid line, thick, square points
set style line 2 lc rgb "steelblue" lt 1 lw 3

plot "data/test2.csv" using 1:2 with linespoints linestyle 1 title "n_e * nu"
