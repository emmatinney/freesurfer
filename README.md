# This is code to use freesurfer on the Northeastern Discovery Cluster

## This is how you visual freesurfer on the cluster
1.	Log into ood.discovery.neu.edu
2.	Open an XFCE terminal 
  a.	Interactive apps, XFCE terminal (alpha)
  b.	Partition- short
  c.	Time - however long you have to work currently 
  d.	No GPU
  e.	CPU-2
  f.	Memory - 2
3.	Once terminal is open:
  a.	Type- “module load freesurfer”
  b.	Type - “export SUBJECTS_DIR=/work/cnelab/TECHS/MRI/BID/sub-Pilot_1/anat/”
  c.	Type - “export SUBJ=subject name”
4. Now we load a subject to check
  a.	Type “ freeview -v $SUBJECTS_DIR/$SUBJ/mri/orig.mgz -v $SUBJECTS_DIR/$SUBJ/mri/brainmask.mgz:colormap=jet:colorscale=0,1:opacity=0.3 -f $SUBJECTS_DIR/$SUBJ/surf/lh.pial:edgecolor='255,0,0' -f $SUBJECTS_DIR/$SUBJ/surf/rh.pial:edgecolor='255,0,0' ”
  c.	Note that you should change subjectID to the actual subject you are working with
  d.	After hitting enter, a Freeview window should open showing you the outputs you specified:
  e.	Use the brain picture boxes to change which orthogonal view appears in the main viewing window. You can use window type to change the organization of the viewing windows. To change which brain slice you are viewing, use the 'Page Up' or 'Page Down' keys on your keyboard or the up and down arrows. (Mac users: press the fn key while using the up and down arrows.)
5.	Now we check the surfaces- locate non brain tissue inside the pial surfaces
  a.	When you are looking for non-brain tissue in the pial surface, the best view to use is often the coronal view. Additionally, it is helpful to turn the various layers (pial surfaces and brainmask volume) on and off, so you can compare them against the anatomy in orig.mgz when deciding whether the boundaries are correct or need editing.
  b.	Make sure the brain mask is covering the entire pial surface
6. Editing
  a.	Select voxel edit
  b.	Set brush value to 0 and eraser value to 1 to erase. Set brush to 1 and eraser to 0 to add. Adjust brush size as needed
  c.	Paint the areas of brainmask.mgz that are incorrectly included within the pial surface. Be careful to make sure “brainmask.mgz” is selected (highlighted) in your list of volumes!
  d.	When you have corrected the defects, save the brainmask.mgz volume!
7. Record what subject you edited, erros, and what you did to resolve
8. Now let's check the white matter
  a.	freeview -v $SUBJECTS_DIR/$SUBJ/mri/orig.mgz -v $SUBJECTS_DIR/$SUBJ/mri/wm.mgz:colormap=heat:opacity=0.1 -f $SUBJECTS_DIR/$SUBJ/surf/lh.white:edgecolor='0,0,0':edgethickness=1 -f $SUBJECTS_DIR/$SUBJ/surf/rh.white:edgecolor='0,0,0':edgethickness=1
  b.	Follow same steps for checking and editing as above
  c.	Record and screenshot errors and what you did to fix. 
9. Now to rerun the subject after fixing the errors:
   recon-all -sd ${SUBJECTS_DIR} -subjid ${SUBJID} -autorecon-pial

## This is how to run the GLM_fit in freesurfer
[See original docs here](https://andysbrainbook.readthedocs.io/en/latest/FreeSurfer/FS_ShortCourse/FS_07_FSGD.html)
1. make sure you have loaded the right free surfer module
  module load freesurfer/6.0.6 (or whichever is newest) 
2. create new dir where all recon-all output dirs are for each subject
  cd /work/cnelab (or your dir)
  mkdir <studyname_FS>
3. copy fsaverage temaplte to study dir 
 cp -R $FREESURFER_HOME/subjects/fsaverage . 
4. define sub dir 
 export SUBJECTS_DIR=`pwd` 
 or 
 setenv SUBJECTS_DIR `pwd` if in tcsh (on cluster it is the former)
4. Create FSGH and Contrasts dirs within study dir: 
 mkdir FSGD Contrasts 
5. Create fsgd file in excel with correct study data 
   see example .FSGD in /work/cnelab/code/freesurfer and in andysbrainbook and save as .txt
6. upload .txt fsgd file to FSGD dir
7. Convert .txt file to .fsgd format
  tr '\r' '\n' < name.txt > name.fsgd 
8. Navigate to Contrast dir and create contrast file- see examples in andybrainbook and here are some common ones  
    to regress a single continuous variable (1st var in .fsgd file) while controlling for 5 covariates (following 4 continuous vars in .fsgd file) with all     vertices in brain mask crate contrast file with the following:
 echo "0 1 0 0 0 0 0" > 1group1var5covars.mtx .
  first 0 indicates group mean (intercept). [See here for more examples](https://surfer.nmr.mgh.harvard.edu/fswiki/Fsgdf1G2V)
to create a two group by continuous variable interaction (e.g., differential effect of age on brain structure in males vs females) with 4 covariates:
 echo "0 0 1 -1 0 0 0 0 0 0 0 0" > 2group1var4covarsall.mtx 
9. Switch shell to tcsh
 tcsh 
10. Navigate to main FS dir
11. Run preprocessing script 
 tcsh runMRIsPreproc.sh studyname
*note study name is same as FSGD file*
13. Run GLM fit script 
 tcsh runGLMs.sh studyname
*note study name is same as FSGD file*
*ensure Contrasts .mtx file is correct for that GLM*
13. Run cluster correction script
 tcsh runClustSims.sh studyname
*note study name is same as FSGD file.*
*Ensure -cache is at 3.0 (p<0.001).*
Note:
There are several options within the .sh files that need to be discussed with the PI and will be dictated based on several factors. For instance, using the --cache option must use value of 3.0 to have a vertex wise threshold of 0.001. r, if -qcache was not flagged during recon all, these cached thresholds wont exist in each subjects fee surfer folders and you will need to use Montecarlo simulations to create vertex-wise thresholds- to do this use the following script:
 tcsh runClustmczsims.sh
More info on cluster and vertex wise corrections can be found tuning the following command: 
 mri_glmfit-sim --help
14. View the results. Navigate to the folders that have been created based on all the input you've done (e.g., lh.thickness.fsgdfilename.10.glmdir) 
Here you should see a file with the same pathname with a .summary extension. At the bottom of that file will be any clusters deemed to be statistically significant. 
rh.thickness.adni.10.glmdir/2group2covar/cache.th30.pos.y.ocn.dat
15. Visualize the results using Freeview 
 freeview -f $SUBJECTS_DIR/fsaverage/surf/rh.inflated:overlay=cache.th13.pos.sig.cluster.mgh

[Original Documentation](https://surfer.nmr.mgh.harvard.edu/fswiki/FreeSurferWiki)
[Tips and Tricks](https://sites.bu.edu/cnrlab/lab-resources/freesurfer-quality-control-guide/freesurfer-quality-control-step-3-fix-the-white-matter-surface/)