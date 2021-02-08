#!/bin/bash
set -ex

module load NCO

ncks -A -v W_SO /project/pr94/lhentge/results_pp_testatlantic/results_ppcc_atl_EXPL/int2lm_out/W_SO_spinup_NOV_selbox_corr2.nc ./output/ifs2lm/laf????1101*.nc
