#!/bin/bash
#SBATCH --time=24:00:0
#SBATCH --nodes=2
#SBATCH --cpus-per-task=8
#SBATCH --mem-per-cpu=32000
#SBATCH --job-name=T1
#SBATCH --partition=short
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=tinney.e@northeastern.edu

export FREESURFER_HOME=$HOME/freesurfer #this is the path for your installed freesurfer folder
source $FREESURFER_HOME/SetUpFreeSurfer.sh
module load freesurfer

recon-all -autorecon-all -sd `pwd` -subjid Pilot_1 -i sub-Pilot_acq-vNav4e_run-01_anat-T1w_1_acq.nii.gz -qcache

 