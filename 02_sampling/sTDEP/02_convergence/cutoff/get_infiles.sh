# Creates the infiles for TDEP to run
# The scripts assumes that you have a infile.ucposcar, infile.ssposcar, infile.lotosplitting and an infile.forceconstants

# First we generate configurations
canonical_configuration --temperature 300 -n 32 --quantum -of 4
# To make a little room in the folder, move the configurations to some folders
rm -rf samples
mkdir samples
mv aims_conf* samples/
# Now we compute the forces
sokrates_compute --folder-model ../module samples/aims_conf* --format=aims --tdep
