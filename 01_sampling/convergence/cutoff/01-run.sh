for rc2 in $(seq -f %04.1f 3.0 1.0 11)
do
	echo $rc2
	mpirun extract_forceconstants --stride 1 --polar -rc2 $rc2 | tee extract_forceconstants_$rc2.log
done

