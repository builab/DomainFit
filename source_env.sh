#!/usr/bin/env bash
# Get the directory of the current script (Not working in Mac)
CHIMERAX_DOMAIN_FIT="/Users/kbui2/Documents/GitHub/chimerax_domain_fit"
AFSCRIPT=/Users/kbui2/Documents/GitHub/chimerax_domain_fit/AlphaFold
#AFSCRIPT=$CHIMERAX_DOMAIN_FIT/AlphaFold
# Add script directory and its subdirectory to the PATH
export PATH=$PATH:$CHIMERAX_DOMAIN_FIT
#export PATH=$PATH:$AFSCRIPT