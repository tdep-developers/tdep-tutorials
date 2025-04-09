# Script to automatize sTDEP for the MgO and Zr tutorials
# This script expect to have an infile.ucposcar and an infile.ssposcar in the folder, and an infile.lotosplitting for polar materials
# This script also expect the module folder for the MLIP to be in the previous folder, ../module
# options:
# --polar -> activate polar flags, expect an infile.lotosplitting file
# --niter X -> Number of iterations to perform, with X an integer
# --nconfs X -> Number of configurations in the first step, with X an integer
# --maximum_frequency X -> Maximum frequency used in the initialization, with X a float
# --cutoff X -> The cutoff for the second order force constants, with X a float

# The temperature
temperature=300
# Is it a polar material ?
ispolar=NO
#Get the number of iteration using --niter, by default it's 5
niter=5
# Just the number of configurations for the start using --nconfs, by default, it will be 4
nconfs=4
# The maximum frequency for the initialization, using --maximum_frequency, by default 20
maxfreq=20.0
# The cutoff for the second order force constants
rc2=10.0
# Do mix ?
mixing=NO
for i in "$@"
do
case $i in
    --polar)
    ispolar=YES
    shift
    ;;
    --mixing)
    mixing=YES
    shift
    ;;
    --nconfs)
    shift
    nconfs=$1
    ;;
    --niter)
    shift
    niter=$1
    ;;
    --maximum_frequency)
    shift
    maxfreq=$1
    ;;
    --temperature)
    shift
    temperature=$1
    ;;
    --cutoff)
    shift
    rc2=$1
    ;;
    *)
    shift
    ;;
esac
done

echo "Is it polar: ${ispolar}"
echo "Are we mixing iterations: ${mixing}"
echo "Number of configurations at the start: ${nconfs}"
echo "Number of iterations: ${niter}"
echo "Maximum frequency for the starting fake phonons: ${maxfreq}"
echo "Temperature: ${temperature}"
echo "Second order cutoff: ${rc2}"
echo " "

if [ "${ispolar}" = "YES" ]
then
    cpfiles='cp ../infile.ucposcar ../infile.ssposcar ../infile.lotosplitting .'
    extractifc='extract_forceconstants -rc2 ${rc2} --polar'
else
    cpfiles='cp ../infile.ucposcar ../infile.ssposcar .'
    extractifc='extract_forceconstants -rc2 ${rc2}'
fi

# We start by cleaning any old results
rm -rf iter.*

# We begin at the 0th iteration - the initialization, and add a padding of zeros for cosmetic
ii=0
printf -v jj "%03d" $ii

# We start with the initialization
mkdir iter.$jj
pushd iter.$jj
    cp ../infile.ucposcar ../infile.ssposcar .
    canonical_configuration --quantum --temperature $temperature -n $nconfs -of 4 --maximum_frequency $maxfreq

    # We get the samples in their own folders to free a bit the main folder
    mkdir -p samples
    for kk in $(seq 1 $nconfs)
    do
        printf -v kkname "%04d" $kk
        mkdir -p samples/sample.$kkname
        mv aims_conf$kkname samples/sample.$kkname/geometry.in
    done
popd

# Keep track of the previous step to compute the force constants
jjm1=$jj
jjm2=$jjm1

# Now we do the steps
for ii in $(seq 1 $niter)
do
    # Just a bit of cosmetic, add padding zeros to the filenames
    printf -v jj "%03d" $ii

    # Get the number of configurations for this step
    nconfs=$(($nconfs*2))

    # Create the folder for the iteration
    folder=iter.$jj
    mkdir -p $folder

    # Go in the folder
    pushd $folder

    # Copy the infiles
    $cpfiles

    # Run the potential
    if [ "${mixing}" = "YES" ] && [ "${ii}" != "1" ]
    then
        samplefiles="../iter.${jjm1}/samples/*/geometry.in ../iter.${jjm2}/samples/*/geometry.in"
    else
        samplefiles="../iter.${jjm1}/samples/*/geometry.in "
    fi
    sokrates_compute --folder-model ../../module $samplefiles --format=aims --tdep

    # Extract the force constants
    $extractifc

    # Link the force constants
    ln -sf outfile.forceconstant infile.forceconstant

    # Extract the phonons
    phonon_dispersion_relations --dos

    # And generate new configurations
    canonical_configuration --quantum --temperature $temperature -n $nconfs -of 4

    # We get the samples in their own folders to free a bit the main folder
    mkdir -p samples
    for kk in $(seq 1 $nconfs)
    do
        printf -v kkname "%04d" $kk
        mkdir -p samples/sample.$kkname
        mv aims_conf$kkname samples/sample.$kkname/geometry.in
    done

    # set the previous steps
    jjm2=$jjm1
    jjm1=$jj

    # and go back to the main folder
    popd
done
