#!/bin/tcsh

setenv study $argv[1]

  foreach hemi (lh rh)
      foreach dir ({$hemi}.thickness.{$study}.10.glmdir)
        mri_glmfit-sim \
          --glmdir {$dir} \
          --mczsim 2 abs \
          --cwp 0.05  \
          --2spaces
  end
end
