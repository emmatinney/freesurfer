#!/bin/bash
#SBATCH --time=24:0:0
#SBATCH --nodes=2
#SBATCH --cpus-per-task=8
#SBATCH --mem-per-cpu=32000
#SBATCH --job-name=reconnall
#SBATCH --partition=short
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=tinney.e@northeastern.edu

#script to submit all subjects for freesurfer reconn all
#first, make a txt file with all subjust names: ls > ../subjects.txt
#make a folder containing all .nii images: cp 0*/MT1__GradWarp__N3m/2*/I*/ADNIDOD_0*_MR_MT1__GradWarp__N3m_Br_2*_*_*.nii /work/cnelab/ADNIDOD/mri/ADNIDOD/freesurfer
#load freesurfer if working on cluster
module load freesurfer
export FREESURFER_HOME=$HOME/freesurfer #this is the path for your installed freesurfer folder
source $FREESURFER_HOME/SetUpFreeSurfer.sh
export FREESURFER=$HOME/freesurfer #this is the path for your installed freesurfer folder
source $FREESURFER/SetUpFreeSurfer.sh
#set working directory
dir=/work/cnelab/practice_recon-all


#open your subject script. wrap command will allow parallel processing for all subjects
#recon-all -autorecon-all -sd 'pwd (this will set working directory to current directory)' -subjid [$whatever your subject id is set as] -i [file.nii] -qcache (allows permissions)

while IFS= read -r s || [ -n "$s" ]; do
    log_file="recon-all_${s}_log.txt"
    error_file="recon-all_${s}_error.txt"

    sbatch --time=24:00:00 --output="$log_file" --error="$error_file" --wrap="recon-all -autorecon-all -sd $(pwd) -subjid $s -i ${dir}/T1s/sub-${s}_ses-1_T1w.nii.gz -qcache"
done < "${dir}/subj.txt"
