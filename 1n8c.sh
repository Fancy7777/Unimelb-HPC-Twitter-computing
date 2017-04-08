#!/bin/bash
#SBATCH -p physical
#SBATCH --time=0:10:00 #hh:mm:ss
#SBATCH --nodes=1
#SBATCH --ntasks=8
#SBATCH --ntasks-per-node=8
module load Python/3.4.3-goolf-2015a
time mpirun -np 8 python deruiw.py
