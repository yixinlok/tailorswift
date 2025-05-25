#!/bin/bash
#SBATCH --account=def-bereyhia
#SBATCH --gpus-per-node=1
#SBATCH --mem=16G               # memory per node
#SBATCH --time=0-00:10
#SBATCH --cpus-per-task=2
module load CCconfig
module load gentoo/2020
module load StdEnv/2020
module load mii/1.1.2
module load imkl/2020.1.217
module load gcc/9.3.0
module load gcccore/.9.3.0
module load ucx/1.8.0
module load libfabric/1.10.1
module load cudacore/.11.1.1
module load cuda/11.1.1
source /lustre03/project/6093715/yixinlok/virtualenv/bin/activate
export PYTHONPATH=$PYTHONPATH:/home/yixinlok/projects/def-bereyhia/yixinlok/tailorswift/src/models

python base_regression_vit.py >> model_test_out/vit_penalty_5.txt 2>&1
       
