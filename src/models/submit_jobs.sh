#!/bin/bash

NAMES=("fitted-skirt")
LEARNING_RATES=(0.001 0.005 0.0001 0.0005)
BATCH_SIZES=(8 16)
EPOCHS=(50 100 150)
N_STOP=(25 35 50)  
MODELS=("base_regression_vit.py")
PENALTIES=(1.0 5.0 8.0 10.0 15.0 20.0 25.0)

for model in "${MODELS[@]}"; do
    for name in "${NAMES[@]}"; do
        for lr in "${LEARNING_RATES[@]}"; do
            for batch in "${BATCH_SIZES[@]}"; do
                for epoch in "${EPOCHS[@]}"; do
                    for stop in "${N_STOP[@]}"; do
                        for penalty in "${PENALTIES[@]}"; do
                        sbatch gput.sh $model $name $lr $batch $epoch $stop $penalty
                        done
                    done
                done
            done
        done
    done
done