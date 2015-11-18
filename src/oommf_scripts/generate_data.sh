#!/bin/bash

# Raise error when a variable is not set, and exit as soon as any
# error occurs in the script.
set -o nounset
set -o errexit

# Define relevant variables; the variable OUTPUT_DIR uses the
# default value '../../data-generated-oommf' but can be set
# by the user before running the script, in which case it will
# use the user-defined value.
OOMMF_SCRIPTS="relaxation_stage.mif dynamic_stage.mif oommf_postprocessing.py"
OUTPUT_DIR=${OUTPUT_DIR:-../../data-generated-oommf}
TIMESTAMP=$(date)

# Create output directory if it does not exist yet
mkdir -p $OUTPUT_DIR

# Copy scripts from source directory to output directory
for FILENAME in $OOMMF_SCRIPTS; do
    cp ./$FILENAME $OUTPUT_DIR/$FILENAME;
done

# Change into the output directory and run all subsequent commands there.
pushd $OUTPUT_DIR
echo "Working in output directory '$OUTPUT_DIR'"

# Generate a README.txt file to inform the user how the data in this
# directory was created.
echo "The data in this directory was automatically generated on $TIMESTAMP
by the script 'src/oommf_scripts/generate_data_oommf.sh' in this repository.
It can safely be deleted if it is no longer needed." > README.txt

# Run the relaxation stage.
tclsh $OOMMFTCL boxsi +fg relaxation_stage.mif -exitondone 1
mv relax-*omf relax.omf

# Run the dynamic stage.
tclsh $OOMMFTCL boxsi +fg dynamic_stage.mif -exitondone 1

# Extract the columns for time, mx, my, mz and store them in the file "dynamic_txyz.txt".
tclsh $OOMMFTCL odtcols < "dynamic.odt" 18 14 15 16 > "dynamic_txyz.txt"

# Extract the spatial magnetisation data to 'mxs.npy', 'mys.npy' and 'mzs.npy'
python oommf_postprocessing.py

# Remove scripts again from this directory
for FILENAME in $OOMMF_SCRIPTS; do
    rm $FILENAME;
done

# Tidy up intermediate files, so that all the remaining files are the
# generated data files we are interested in.
rm -f *.omf
rm -f *.odt

echo
echo "Successfully generated OOMMF data in directory: '$OUTPUT_DIR'"
echo
