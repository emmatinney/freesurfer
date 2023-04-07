#!/bin/tcsh

setenv study $argv[1]

foreach meas (area thickness)
  foreach hemi (lh rh)
    foreach smoothness (10)
      foreach dir ({$hemi}.{$meas}.{$study}.{$smoothness}.glmdir)
        mri_glmfit-sim \
          --glmdir {$dir} \
          --cache 3.0 pos \
          --cwp 0.05  \
          --2spaces
      end
    end
  end
end