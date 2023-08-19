temp=1100

fc: infile.forceconstant
compute: infile.forces

infile.forces:
	tdep_ln_previous_samples
	sokrates_compute --folder-model ../../module/ samples*/*/geometry.in --tdep

infile.forceconstant: infile.forces
	extract_forceconstants -rc2 10 -U0 | tee extract_forceconstants.log
	ln -sf outfile.forceconstant infile.forceconstant
	phonon_dispersion_relations --dos --temperature $(temp) -qg 12 12 12 -p && gnuplot -p outfile.dispersion_relations.gnuplot_pdf

iteration: infile.forceconstant
	tdep_create_next_iteration --max-samples 1024 -T $(temp)

init:
	generate_structure -na 128
	mv outfile.ssposcar infile.ssposcar
	canonical_configuration -n 128 -t $(temp)
	tdep_create_sample_folders contcar_conf*

clean:
	rm -f outfile.* 
	rm -f extract_forceconstants.log
	rm -f infile.forceconstant infile.forces infile.meta infile.positions infile.stat
	rm -rf samples*
