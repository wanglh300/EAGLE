#! /bin/bash

python test.py \
    --cates airplane \
    --resume_checkpoint  checkpoints/ae/shapenet15k-cateairplane/checkpoint-899.pt \
    --dims 512-512-512 \
    --use_deterministic_encoder \
    --evaluate_recon
