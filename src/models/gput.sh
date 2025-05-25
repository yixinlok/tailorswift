#!/bin/bash
#SBATCH --account=def-bereyhia
#SBATCH --gpus-per-node=1
#SBATCH --mem=16G               # memory per node
#SBATCH --time=0-04:00
#SBATCH --cpus-per-task=4 
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

MODEL=$1
NAME=$2
LR=$3
BATCH_SIZE=$4
EPOCHS=$5
N_STOP=$6
PENALTY=$7

RESULTS=$(python $MODEL --name $NAME --learning_rate $LR --batch_size $BATCH_SIZE --epochs $EPOCHS --n_stop $N_STOP --penalty $PENALTY)

TEMP_FILE="temp_results_${SLURM_JOB_ID}.csv"

echo "$MODEL,$NAME,$LR,$BATCH_SIZE,$EPOCHS,$N_STOP,$PENALTY,\"$RESULTS\"" >> "$TEMP_FILE"
echo "" >> "$TEMP_FILE"

cat "$TEMP_FILE" >> results.csv
rm "$TEMP_FILE"
