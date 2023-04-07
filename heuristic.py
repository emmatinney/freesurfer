##to run do sh run_heudiconv.sh heuristic.py

"""Heuristic to convert dicoms to nifti in Brain Imaging Data Structure format
for the R33 realtime schizophrenia project.

Use this heuristic with [heudiconv](https://github.com/nipy/heudiconv).


Scanning paradigm and session names
-----------------

    - Day 1: localizer
    - Day 2: nf1
    - Day 3: nf2
    - Day 4: nf3
    - Day 5: nf4

"""


def create_key(template, outtype=('nii.gz',), annotation_classes=None):
    if template is None or not template:
        raise ValueError('Template must be a valid format string')
    return (template, outtype, annotation_classes)


def infotodict(seqinfo):
    """Heuristic evaluator for determining which items belong where

    allowed template fields - follow python string module:

    item: index within category
    subject: participant id
    seqitem: item number during scanning
    subindex: sub index within group
    """

    t1 = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_T1w')
    t2 = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_T2w')

    restbl = create_key(
        'sub-{subject}/{session}/func/sub-{subject}_{session}_task-restbl_run-{item:02d}_bold')
    restpre = create_key(
        'sub-{subject}/{session}/func/sub-{subject}_{session}_task-restpre_run-{item:02d}_bold')
    restpost = create_key(
        'sub-{subject}/{session}/func/sub-{subject}_{session}_task-restpost_run-{item:02d}_bold')
    fmap = create_key(
        'sub-{subject}/{session}/fmap/sub-{subject}_{session}_dir-{dir}_run-{item:02d}_epi')

    selfother = create_key(
        'sub-{subject}/{session}/func/sub-{subject}_{session}_task-selfother_run-{item:02d}_bold')
    selfref = create_key(
        'sub-{subject}/{session}/func/sub-{subject}_{session}_task-selfref_run-{item:02d}_bold')
    cpt = create_key(
        'sub-{subject}/{session}/func/sub-{subject}_{session}_task-cpt_run-{item:02d}_bold')
    transferpre = create_key(
        'sub-{subject}/{session}/func/sub-{subject}_{session}_task-transferpre_run-{item:02d}_bold')
    transferpost = create_key(
        'sub-{subject}/{session}/func/sub-{subject}_{session}_task-transferpost_run-{item:02d}_bold')
    feedback= create_key(
        'sub-{subject}/{session}/func/sub-{subject}_{session}_task-feedback_run-{item:02d}_bold')

    
    dwi = create_key(
        'sub-{subject}/{session}/dwi/sub-{subject}_{session}_dir-{dir}_run-{item:02}_dwi')

    info = {
        t1: [],
        t2: [],
        restbl: [],
        restpre: [],
        restpost: [],
        fmap: [],
        dwi: [],
        selfother: [],
        selfref: [],
        cpt: [],
        transferpre: [],
        transferpost: [],
        feedback: []
    }

    for s in seqinfo:

        # T1.
        if (s.dim1, s.dim2, s.dim3, s.dim4) == (256, 256, 176, 1) and 'T1w' in s.protocol_name and not s.is_motion_corrected:
            info[t1] = [s.series_id]

        # T2.
        elif s.dim3 == 176 and s.dim4 == 1 and 'T2w' in s.protocol_name and not s.is_motion_corrected:
            info[t2].append(s.series_id)

        # Resting state (AP and PA).
        elif s.dim4 > 100 and 'task-restbl' in s.protocol_name and not s.is_motion_corrected:
            info[restbl].append(s.series_id)
            #uncoment this if you want to include direction else run-01 is PA and run-02 ia AP
         #if s.protocol_name.endswith('AP'):
              #  info[resting_state].append({'item': s.series_id, 'dir': 'ap'})
            #elif s.protocol_name.endswith('PA'):
             #   info[resting_state].append({'item': s.series_id, 'dir': 'pa'})
        elif s.dim4 > 100 and 'task-restpre' in s.protocol_name and not s.is_motion_corrected:
            info[restpre].append(s.series_id)
        elif s.dim4 > 100 and 'task-restpost' in s.protocol_name and not s.is_motion_corrected:
            info[restpost].append(s.series_id)
       
       
        # fmap (AP and PA).
        elif (s.dim1, s.dim2, s.dim3, s.dim4) == (128, 128, 68, 3) and 'fmap' in s.protocol_name:
            if 'AP' in s.protocol_name:
                info[fmap].append({'dir': 'AP', 'item': s.series_id})
            elif 'PA' in s.protocol_name:
                info[fmap].append({'dir': 'PA', 'item': s.series_id})

        # fMRI selfother task.
        elif s.dim4 > 190 and 'task-selfother' in s.protocol_name: #random value fo dim 4
            info[selfother].append(s.series_id)
   #uncoment this if you want to include direction else run-01 is PA and run-02 ia AP
         #if s.protocol_name.endswith('AP'):
              #  info[resting_state].append({'item': s.series_id, 'dir': 'ap'})
            #elif s.protocol_name.endswith('PA'):
             #   info[resting_state].append({'item': s.series_id, 'dir': 'pa'})

        # fMRI self reference task.
        elif s.dim4 > 200 and 'task-selfref' in s.protocol_name:
            info[selfref].append(s.series_id)
   #uncoment this if you want to include direction else run-01 is PA and run-02 ia AP
         #if s.protocol_name.endswith('AP'):
              #  info[resting_state].append({'item': s.series_id, 'dir': 'ap'})
            #elif s.protocol_name.endswith('PA'):
             #   info[resting_state].append({'item': s.series_id, 'dir': 'pa'})

        # fMRI CPT task.
        elif s.dim4 > 100 and 'task-cpt' in s.protocol_name: #random value fo dim 4
            info[cpt].append(s.series_id)
   #uncoment this if you want to include direction else run-01 is PA and run-02 ia AP
         #if s.protocol_name.endswith('AP'):
              #  info[resting_state].append({'item': s.series_id, 'dir': 'ap'})
            #elif s.protocol_name.endswith('PA'):
             #   info[resting_state].append({'item': s.series_id, 'dir': 'pa'})

        # fMRI CPT task
        #elif s.dim4 == 100 and 'task-cpt' in s.protocol_name:
            #info[cpt].append(s.series_id)

        # STG, SMC or DMN feedback tasks.
        # QUESTION(kaczmarj): what should the cutoff for timeseries be? Normal is 96.
        elif s.dim4 > 80 and 'task-transferpre' in s.protocol_name:
            info[transferpre].append(s.series_id)
        elif s.dim4 > 80 and 'task-transferpost' in s.protocol_name:
            info[transferpost].append(s.series_id)
        elif s.dim4 > 80 and 'task-feedback' in s.protocol_name :
            info[feedback].append(s.series_id)

        # Diffusion (AP and PA).
        elif (s.dim1, s.dim2, s.dim3, s.dim4) == (140, 140, 92, 100) and 'dwi' in s.protocol_name:
            if 'AP' in s.protocol_name:
                info[dwi].append({'dir': 'AP', 'item': s.series_id})
            elif 'PA' in s.protocol_name:
                info[dwi].append({'dir': 'AP', 'item': s.series_id})

    return info