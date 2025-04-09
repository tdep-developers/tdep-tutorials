for ii in 001 002 004 008 016 032 064 128 256 512
do
        # Create the folder for this stride
	folder=stride_$ii
	mkdir -p $folder
        # Go in this folder
	pushd $folder
        # Make a link of the input file needed by TDEP
	ln -sf ../infile.forces
	ln -sf ../infile.positions
	ln -sf ../infile.ucposcar
	ln -sf ../infile.ssposcar
	ln -sf ../infile.meta
	ln -sf ../infile.stat
	ln -sf ../infile.lotosplitting
        # Then extract the force constants
        extract_forceconstants -rc2 10 --polar --stride $ii
        ln -sf outfile.forceconstant infile.forceconstant
        # And extract the phonons
        phonon_dispersion_relations --dos
	popd
done

