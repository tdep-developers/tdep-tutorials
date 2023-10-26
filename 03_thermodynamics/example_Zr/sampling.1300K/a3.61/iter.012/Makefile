temp=1300

fc:
	extract_forceconstants -rc2 10 -U0 | tee extract_forceconstants.log

dos:
	ln -sf outfile.forceconstant infile.forceconstant
	phonon_dispersion_relations --dos --temperature $(temp) -qg 4 4 4 -p && gnuplot -p outfile.dispersion_relations.gnuplot_pdf

clean:
	rm -f outfile.* 
	rm -f extract_forceconstants.log
	rm -f infile.forceconstant
