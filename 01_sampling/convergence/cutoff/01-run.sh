for rc2 in $(seq -f %04.1f 2.5 0.5 9)
do
	echo $rc2
	folder=rc_polar_$rc2
	# folder=rc_nopolar_$rc2
	mkdir $folder
	mpirun extract_forceconstants --polar --stride 1 -rc2 $rc2 | tee extract_forceconstants.log
	# mpirun extract_forceconstants --stride 1 -rc2 $rc2 | tee extract_forceconstants.log
	ln -sf outfile.forceconstant infile.forceconstant
	tdep_plot_fc_norms
	phonon_dispersion_relations -p --dos && gnuplot -p outfile.dispersion_relations.gnuplot_pdf
	mv fc_norms.pdf outfile.forceconstant outfile.phonon_dos outfile.U0 outfile.dispersion_relations.pdf extract_forceconstants.log $folder
	# restore reference forceconstants
	ln -sf ../infile.forceconstant
done

