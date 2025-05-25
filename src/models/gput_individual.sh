#!/bin/bash

sbatch gput.sh base_regression_vit.py collar 0.000001 16 150 25 1.0

sbatch gput.sh base_regression_vit.py collar 0.00005 16 50 25 1.0

sbatch gput.sh base_regression_vit.py collar 0.00001 8 150 35 1.0