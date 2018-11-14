#!/bin/bash
set -e

BASE_DIR=/home/ckoziol/Documents/Python/fenics/fenics_ice
RUN_DIR=$BASE_DIR/runs

INPUT_DIR=$BASE_DIR/output/smith/smith_alpha_lcurve/run1e6

OUTPUT_DIR=$BASE_DIR/output/smith/smith_beta_lcurve


OUT1en3=$OUTPUT_DIR/run1en3
OUT1en2=$OUTPUT_DIR/run1en2
OUT1en1=$OUTPUT_DIR/run1en1
OUT1e0=$OUTPUT_DIR/run1e0
OUT1e1=$OUTPUT_DIR/run1e1
OUT1e2=$OUTPUT_DIR/run1e2
OUT1e3=$OUTPUT_DIR/run1e3
OUT1e4=$OUTPUT_DIR/run1e4
OUT1e5=$OUTPUT_DIR/run1e5
OUT1e6=$OUTPUT_DIR/run1e6
OUT1e7=$OUTPUT_DIR/run1e7
OUT1e8=$OUTPUT_DIR/run1e8
OUT1e9=$OUTPUT_DIR/run1e9

NX=225
NY=189



source activate dolfinproject_py3
cd $RUN_DIR

python run_inv.py -x $NX -y $NY -m 40 -p 1  -r 1.0 1e-30 1e-9 1e-30 1e-3 -d $INPUT_DIR -o $OUT1en3
python run_inv.py -x $NX -y $NY -m 40 -p 1  -r 1.0 1e-30 1e-9 1e-30 1e-2 -d $INPUT_DIR -o $OUT1en2
python run_inv.py -x $NX -y $NY -m 40 -p 1  -r 1.0 1e-30 1e-9 1e-30 1e-1 -d $INPUT_DIR -o $OUT1en1
python run_inv.py -x $NX -y $NY -m 40 -p 1  -r 1.0 1e-30 1e-9 1e-30 1e0 -d $INPUT_DIR -o $OUT1e0
python run_inv.py -x $NX -y $NY -m 40 -p 1  -r 1.0 1e-30 1e-9 1e-30 1e1 -d $INPUT_DIR -o $OUT1e1
python run_inv.py -x $NX -y $NY -m 40 -p 1  -r 1.0 1e-30 1e-9 1e-30 1e2 -d $INPUT_DIR -o $OUT1e2
python run_inv.py -x $NX -y $NY -m 40 -p 1  -r 1.0 1e-30 1e-9 1e-30 1e3 -d $INPUT_DIR -o $OUT1e3
python run_inv.py -x $NX -y $NY -m 40 -p 1  -r 1.0 1e-30 1e-9 1e-30 1e4 -d $INPUT_DIR -o $OUT1e4
python run_inv.py -x $NX -y $NY -m 40 -p 1  -r 1.0 1e-30 1e-9 1e-30 1e5 -d $INPUT_DIR -o $OUT1e5
python run_inv.py -x $NX -y $NY -m 40 -p 1  -r 1.0 1e-30 1e-9 1e-30 1e6 -d $INPUT_DIR -o $OUT1e6
python run_inv.py -x $NX -y $NY -m 40 -p 1  -r 1.0 1e-30 1e-9 1e-30 1e7 -d $INPUT_DIR -o $OUT1e7
python run_inv.py -x $NX -y $NY -m 40 -p 1  -r 1.0 1e-30 1e-9 1e-30 1e8 -d $INPUT_DIR -o $OUT1e8
python run_inv.py -x $NX -y $NY -m 40 -p 1  -r 1.0 1e-30 1e-9 1e-30 1e9 -d $INPUT_DIR -o $OUT1e9
