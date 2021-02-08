#!/bin/bash -l
#
#SBATCH --time=15:00:00
#SBATCH --nodes=1
#SBATCH --partition=normal
#SBATCH --output=out.compress.%j
#SBATCH --error=err.compress.%j
#SBATCH --constraint=gpu
#SBATCH --account=pr94

set -ex

module load daint-gpu
module load NCO

echo starting
echo `date`

SIMDIR=${1}  #04120100_ppcc_atl_EXPL_04_reproduce
echo $SIMDIR

/users/demorym/bin/nczip -r $SIMDIR/1h
/users/demorym/bin/nczip -r $SIMDIR/1h_clearsky
/users/demorym/bin/nczip -r $SIMDIR/1h_rad
/users/demorym/bin/nczip -r $SIMDIR/1h_second
/users/demorym/bin/nczip -r $SIMDIR/1h_vertint
/users/demorym/bin/nczip -r $SIMDIR/24_h
/users/demorym/bin/nczip -r $SIMDIR/3h
/users/demorym/bin/nczip -r $SIMDIR/6h
/users/demorym/bin/nczip -r $SIMDIR/6h_3D
/users/demorym/bin/nczip -r $SIMDIR/6h_3D_second

echo finished
echo `date`
