# Unimelb-HPC-Twitter-computing
Unimelb Cluster and Cloud computing assignment 1 by implementing the program in Spartan

# How to use
If you wanna try this, you need to initially have a Spartan account.
Then you need to copy deruiw.py, 1n1c.sh, 1n8c.sh, 2n8c.sh to the account.

### Running Local
Well before this, you need to install mpi on your computer. 

```batch
mpirun -n 1 python deruiw.py
```
### Install mpi on mac
I am using MacOS sierra, Pythong 2.7 (I don't think python version makes any difference so just try it)
1. Install X-code, open it and update what ever it tells you.

       1.1 launch terminal execute command:

                 $ xcode-select --install

                 $ ln -s  ~/.bash_frofile  ~/.bashrc

2. download the source code form   https://www.open-mpi.org/software/ompi/v2.1/    Usually you may choose openmpi-2.1.0.tar.gz

     then commandline again:

                  2.1    $ tar zxvf openmpi-2.1.0.tar.gz

                  2.2    $ ./configure --prefix=/usr/local

                  2.3    $ make all

                  2.4    $ sudo make install

3. Then finally use     $ pip install MPI4py

### Running on Spartan

```commandline
sbatch 1n1c.sh
sbatch 1n8c.sh
sbatch 2n8c.sh
```
Then you will receive a result file with an ending '.out'.

The detial is including in the report
My result will also be included.
