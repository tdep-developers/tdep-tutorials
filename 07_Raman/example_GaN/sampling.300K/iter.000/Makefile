temp=300

fc: infile.forceconstant
compute: infile.forces

infile.forces:
	tdep_ln_previous_samples
	sokrates_compute --folder-model ../../module/ samples*/*/geometry.in --tdep

infile.forceconstant: infile.forces
	extract_forceconstants --polar -rc2 7 -U0 | tee extract_forceconstants.log
	ln -sf outfile.forceconstant infile.forceconstant
	phonon_dispersion_relations -p && gnuplot -p outfile.dispersion_relations.gnuplot_pdf

iteration: infile.forceconstant
	tdep_create_next_iteration --max-samples 1024 -T $(temp)

init:
	canonical_configuration -n 4 -t $(temp) -mf 15 --quantum
	tdep_create_sample_folders contcar_conf*

clean:
	rm -f outfile.* 
	rm -f extract_forceconstants.log
	rm -f infile.forceconstant infile.forces infile.meta infile.positions infile.stat
	rm -rf samples*
