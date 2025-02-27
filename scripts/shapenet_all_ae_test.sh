#! /bin/bash

python test.py \
    --cates all \
    --resume_checkpoint checkpoints/ae/shapenet15k-cateall/checkpoint-latest.pt \
    --dims 512-512-512 \
    --use_deterministic_encoder \
    --evaluate_recon \
    --resume_dataset_mean checkpoints/ae/shapenet15k-cateall/train_set_mean.npy \
    --resume_dataset_std checkpoints/ae/shapenet15k-cateall/train_set_std.npy

