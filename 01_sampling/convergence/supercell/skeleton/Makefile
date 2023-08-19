samples:
	ln -sf ../infile.forceconstant
	ln -sf ../infile.lotosplitting
	canonical_configuration --temperature 300 --quantum -n 512
	tdep_create_sample_folders contcar_conf*

infile.forces: samples
	sokrates_compute --float32 --tdep --folder-model ../../module/ samples*/sample.*/geometry.in

folders: stride_001

stride_001: infile.forces
	bash 00-prepare_folders.sh

run: stride_001
	bash 01-run_folders.sh

clean:
	rm -r stride_*
	
