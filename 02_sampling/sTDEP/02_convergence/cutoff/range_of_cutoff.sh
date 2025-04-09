# Run extract_forceconstants for a range of cutoff
for rc2 in $(seq -f %04.1f 2.5 0.5 9)
do
        # We will put the result in their own folder
	echo $rc2
	folder=rc_polar_$rc2
	mkdir $folder
        # Go in the folder
        pushd $folder
        # Make a link of the input file needed by TDEP
	ln -sf ../infile.forces
	ln -sf ../infile.positions
	ln -sf ../infile.ucposcar
	ln -sf ../infile.ssposcar
	ln -sf ../infile.meta
	ln -sf ../infile.stat
	ln -sf ../infile.lotosplitting
        # We run extract_forceconstants with the current cutoff, and keep the log
	extract_forceconstants --polar --stride 1 -rc2 $rc2 | tee extract_forceconstants.log
        # We compute the norm of the IFC with respect to distance
	ln -sf outfile.forceconstant infile.forceconstant
	tdep_plot_fc_norms
        # We compute the phonons
	phonon_dispersion_relations -p --dos
        # And we go back to the root directory
	popd
done
