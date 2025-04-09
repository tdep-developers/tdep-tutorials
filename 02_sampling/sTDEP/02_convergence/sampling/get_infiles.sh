# Creates the infiles for TDEP to run
# The scripts assumes that you have a infile.ucposcar, infile.ssposcar, infile.lotosplitting and an infile.forceconstants

# Let's start by generating a supercell
generate_structure -na 216
# And put it as an input
mv outfile.ssposcar infile.ssposcar
# First we generate configurations
canonical_configuration --temperature 300 -n 512 --quantum -of 4
# To keep a trace of the original forceconstants, as they would be overwritten otherwise
mv infile.forceconstant original.forceconstant
# To make a little room in the folder, move the configurations to some folders
rm -rf samples
mkdir samples
mv aims_conf* samples/
# Now we compute the forces
sokrates_compute --folder-model ../module samples/aims_conf* --format=aims --tdep
