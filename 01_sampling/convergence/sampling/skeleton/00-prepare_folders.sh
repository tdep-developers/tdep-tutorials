for ii in 001 002 004 008 016 032 064 128 256 512
do
	folder=stride_$ii
	mkdir -p $folder
	pushd $folder
	ln -sf ../infile.forces
	ln -sf ../infile.positions
	ln -sf ../infile.ucposcar
	ln -sf ../infile.ssposcar
	ln -sf ../infile.meta
	ln -sf ../infile.stat
	ln -sf ../../infile.lotosplitting
	popd

	cat Makefile.template | sed -e "s,STRIDE,$ii,g" > $folder/Makefile
done

