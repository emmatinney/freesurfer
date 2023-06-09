#!/bin/tcsh

setenv study $argv[1]

foreach hemi (lh rh)
  foreach smoothing (10)
    foreach meas (area thickness)
      mris_preproc --fsgd FSGD/{$study}.fsgd \
        --cache-in {$meas}.fwhm{$smoothing}.fsaverage \
        --target fsaverage \
        --hemi {$hemi} \
        --out {$hemi}.{$meas}.{$study}.{$smoothing}.mgh
    end
  end
end
