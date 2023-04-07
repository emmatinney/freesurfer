#!/bin/tcsh

set study = $argv[1]

foreach hemi (lh rh)
        mri_glmfit \
        --y {$hemi}.thickness.{$study}.10.mgh \
        --fsgd FSGD/{$study}.fsgd \
        --C Contrasts/ace_eela_t.mtx \
        --surf fsaverage {$hemi}  \
        --cortex \
        --glmdir {$hemi}.thickness.{$study}.10.glmdir
end
