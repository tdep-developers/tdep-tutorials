run: infile.forces
	bash 01-run.sh

infile.forces: samples
	sokrates_compute --float32 --tdep --folder-model ../module/ samples*/sample.*/geometry.in

samples:
	canonical_configuration --temperature 300 --quantum -n 128
	tdep_create_sample_folders contcar_conf*

clean:
	rm -f extract_force*.log
	rm -f outfile.*
	rm -f infile.forces
	rm -f infile.meta
	rm -f infile.positions
	rm -f infile.stat
	rm -rf samples
	
