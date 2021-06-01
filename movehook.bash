#!/bin/bash -l
#
#SBATCH --time=11:00:00
#SBATCH --ntasks=1
#SBATCH --partition=xfer
#SBATCH --output=out.move.%j
#SBATCH --error=err.move.%j
#SBATCH --mem=6000

unset SLURM_MEM_PER_CPU

echo starting
echo `date`

CURDIR=$(pwd)

SIMDIR=${1}
#read the year from filename
cd $SIMDIR/24h
YYYY=$(ls lffd??????????0000.nc | head -1 | cut -c 5-8)

cd $CURDIR

DESTDIR=/store/c2sm/ch4/robro/RUN_COSMO/atlantic/${2}/${YYYY}

if [ ! -d ${DESTDIR} ]
then
 mkdir -p ${DESTDIR}
fi

srun rsync -r $SIMDIR/1h $DESTDIR
srun rsync -r $SIMDIR/1h_clearsky $DESTDIR
srun rsync -r $SIMDIR/1h_rad $DESTDIR
srun rsync -r $SIMDIR/1h_second $DESTDIR
srun rsync -r $SIMDIR/1h_vertint $DESTDIR
srun rsync -r $SIMDIR/24h $DESTDIR
srun rsync -r $SIMDIR/3h $DESTDIR
srun rsync -r $SIMDIR/6h $DESTDIR
srun rsync -r $SIMDIR/6h_3D $DESTDIR
srun rsync -r $SIMDIR/6h_3D_second $DESTDIR
srun rsync -r $SIMDIR/job_logs $DESTDIR
srun rsync -r $SIMDIR/restarts $DESTDIR
srun rsync -r $SIMDIR/lffd*c.nc $DESTDIR

echo finished
echo `date`

