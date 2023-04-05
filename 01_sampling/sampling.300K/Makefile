rc2 = 0

input:
	tdep_parse_output samples/*/OUTPUT --format FORMAT

fc: input
	extract_forceconstants -rc2 $(rc2) 2>&1 | tee extract_forceconstants.log
	ln -sf outfile.forceconstant infile.forceconstant
	phonon_dispersion_relations -p
	gnuplot -p outfile.dispersion_relations.gnuplot_pdf
	plot_fc_norms

all: fc

