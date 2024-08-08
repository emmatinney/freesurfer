# Freesurfer on the Northeastern Discovery Cluster
## This is how you run recon-all on the cluster
reconnall_T1.sh runs one subject at a time. you will need to configure the file to direct it to the correct path.
```
export FREESURFER_HOME=$HOME/freesurfer #this is the path for your installed freesurfer folder
source $FREESURFER_HOME/SetUpFreeSurfer.sh
module load freesurfer
recon-all -autorecon-all -sd `pwd` -subjid SUBJID -i *.nii.gz -qcache
```
recon_all.sh runs multiple subjects at a time in parallel
```
export FREESURFER_HOME=$HOME/freesurfer #this is the path for your installed freesurfer folder
source $FREESURFER_HOME/SetUpFreeSurfer.sh
module load freesurfer
dir=/work/cnelab/practice_recon-all
while IFS= read -r s || [ -n "$s" ]; do
    log_file="recon-all_${s}_log.txt"
    error_file="recon-all_${s}_error.txt"

    sbatch --time=24:00:00 --output="$log_file" --error="$error_file" --wrap="recon-all -autorecon-all -sd $(pwd) -subjid $s -i ${dir}/T1s/sub-${s}_ses-1_T1w.nii.gz -qcache"
done < "${dir}/subj.txt"
```
## This is how you extract individual subject data on the cluster
You can extract individual subject data from multiple subjects and import them to a table quite easily with freesurfer functions, [asegstats2table](https://surfer.nmr.mgh.harvard.edu/fswiki/asegstats2table) and [aparcstats2table](https://surfer.nmr.mgh.harvard.edu/fswiki/aparcstats2table). 
```
asegstats2table --subjects sub1 sub2 sub3 sub4 --meas volume --tablefile aseg_stats.txt
aparcstats2table --subjects sub1 sub2 sub3 sub4 --hemi rh --meas thickness --tablefile aparc_stats.txt
```
enter the hemisphere, (rh or lh), and measure you wish to extract. for aparc default is area (alt volume, thickness, thicknessstd, meancurv, gauscurv, foldind, curvind). for aseg there are only two options, volume or mean.
## This is how you visual freesurfer on the cluster
1.	Log into ood.discovery.neu.edu
2.	Open an XFCE terminal
  * Interactive apps, XFCE terminal (alpha)
  * Partition- short
  * Time - however long you have to work currently 
  * No GPU
  * CPU-2
  * Memory - 2
4.	Once terminal is open:
```
module load freesurfer
export SUBJECTS_DIR=/work/cnelab/TECHS/MRI/BID/sub-Pilot_1/anat/
export SUBJ=SUBJID
```
5. Now we load a subject to check
```
freeview -v $SUBJECTS_DIR/$SUBJ/mri/orig.mgz -v $SUBJECTS_DIR/$SUBJ/mri/brainmask.mgz:colormap=jet:colorscale=0,1:opacity=0.3 -f $SUBJECTS_DIR/$SUBJ/surf/lh.pial:edgecolor='255,0,0' -f $SUBJECTS_DIR/$SUBJ/surf/rh.pial:edgecolor='255,0,0'
```
  * Note that you should change subjectID to the actual subject you are working with
  * After hitting enter, a Freeview window should open showing you the outputs you specified:
  * Use the brain picture boxes to change which orthogonal view appears in the main viewing window. You can use window type to change the organization of the viewing windows. To change which brain slice you are viewing, use the 'Page Up' or 'Page Down' keys on your keyboard or the up and down arrows. (Mac users: press the fn key while using the up and down arrows.)
6.	Now we check the surfaces- locate non brain tissue inside the pial surfaces
  * When you are looking for non-brain tissue in the pial surface, the best view to use is often the coronal view. Additionally, it is helpful to turn the various layers (pial surfaces and brainmask volume) on and off, so you can compare them against the anatomy in orig.mgz when deciding whether the boundaries are correct or need editing.
  * Make sure the brain mask is covering the entire pial surface
7. Editing
  * Select voxel edit
  * Set brush value to 0 and eraser value to 1 to erase. Set brush to 1 and eraser to 0 to add. Adjust brush size as needed
  * Paint the areas of brainmask.mgz that are incorrectly included within the pial surface. Be careful to make sure “brainmask.mgz” is selected (highlighted) in your list of volumes!
  * When you have corrected the defects, save the brainmask.mgz volume!
8. Record what subject you edited, erros, and what you did to resolve
9. Now let's check the white matter
```
freeview -v $SUBJECTS_DIR/$SUBJ/mri/orig.mgz -v $SUBJECTS_DIR/$SUBJ/mri/wm.mgz:colormap=heat:opacity=0.1 -f $SUBJECTS_DIR/$SUBJ/surf/lh.white:edgecolor='0,0,0':edgethickness=1 -f $SUBJECTS_DIR/$SUBJ/surf/rh.white:edgecolor='0,0,0':edgethickness=1
```
  * Follow same steps for checking and editing as above
  * Record and screenshot errors and what you did to fix. 
10. Now to rerun the subject after fixing the errors:
```
recon-all -sd ${SUBJECTS_DIR} -subjid ${SUBJID} -autorecon-pial
```
## This is how to run the GLM_fit in freesurfer
[See original docs here](https://andysbrainbook.readthedocs.io/en/latest/FreeSurfer/FS_ShortCourse/FS_07_FSGD.html)
1. make sure you have loaded the right free surfer module
  * module load freesurfer/6.0.6 (or whichever is newest) 
2. create new dir where all recon-all output dirs are for each subject
```
cd /work/cnelab (or your dir)
mkdir <studyname_FS>
```
3. copy fsaverage temaplte to study dir 
```
cp -R $FREESURFER_HOME/subjects/fsaverage .
``` 
4. define sub dir 
```
export SUBJECTS_DIR=`pwd` 
 *or* 
setenv SUBJECTS_DIR `pwd` if in tcsh (on cluster it is the former)
```
4. Create FSGH and Contrasts dirs within study dir: 
```
mkdir FSGD Contrasts
```
5. Create fsgd file in excel with correct study data 
  *  see example .FSGD in /work/cnelab/code/freesurfer and in andysbrainbook and save as .txt
6. upload .txt fsgd file to FSGD dir
7. Convert .txt file to .fsgd format
```
tr '\r' '\n' < name.txt > name.fsgd
```
8. Navigate to Contrast dir and create contrast file- see examples in andybrainbook and here are some common ones  
  * to regress a single continuous variable (1st var in .fsgd file) while controlling for 5 covariates (following 4 continuous vars in .fsgd file) with all     vertices in brain mask crate contrast file with the following:
```
echo "0 1 0 0 0 0 0" > 1group1var5covars.mtx .
```
  *  first 0 indicates group mean (intercept). [See here for more examples](https://surfer.nmr.mgh.harvard.edu/fswiki/Fsgdf1G2V)
to create a two group by continuous variable interaction (e.g., differential effect of age on brain structure in males vs females) with 4 covariates:
```
echo "0 0 1 -1 0 0 0 0 0 0 0 0" > 2group1var4covarsall.mtx
```
9. Switch shell to tcsh
```
tcsh
```
10. Navigate to main FS dir
11. Run preprocessing script 
```
tcsh runMRIsPreproc.sh studyname
```
*note study name is same as FSGD file*
13. Run GLM fit script 
```
tcsh runGLMs.sh studyname
```
*note study name is same as FSGD file*
*ensure Contrasts .mtx file is correct for that GLM*

13. Run cluster correction script
```
tcsh runClustSims.sh studyname
```
*note study name is same as FSGD file.*
*Ensure -cache is at 3.0 (p<0.001).*
Note:
  * There are several options within the .sh files that need to be discussed with the PI and will be dictated based on several factors. For instance, using the --cache option must use value of 3.0 to have a vertex wise threshold of 0.001. r, if -qcache was not flagged during recon all, these cached thresholds wont exist in each subjects fee surfer folders and you will need to use Montecarlo simulations to create vertex-wise thresholds- to do this use the following script:
```
tcsh runClustmczsims.sh
```
  * More info on cluster and vertex wise corrections can be found tuning the following command: 
```
mri_glmfit-sim --help
```
14. View the results. Navigate to the folders that have been created based on all the input you've done (e.g., lh.thickness.fsgdfilename.10.glmdir) 
  * Here you should see a file with the same pathname with a .summary extension. At the bottom of that file will be any clusters deemed to be statistically significant. 
  * rh.thickness.adni.10.glmdir/2group2covar/cache.th30.pos.y.ocn.dat
15. Visualize the results using Freeview 
```
freeview -f $SUBJECTS_DIR/fsaverage/surf/rh.inflated:overlay=cache.th13.pos.sig.cluster.mgh
```
[Original Documentation](https://surfer.nmr.mgh.harvard.edu/fswiki/FreeSurferWiki) & [Tips and Tricks](https://sites.bu.edu/cnrlab/lab-resources/freesurfer-quality-control-guide/freesurfer-quality-control-step-3-fix-the-white-matter-surface/)
