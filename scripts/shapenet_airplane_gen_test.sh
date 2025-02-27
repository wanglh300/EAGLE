#! /bin/bash

python test.py \
    --cates chair \
    --resume_checkpoint checkpoints/gen/shapenet15k-catechair-seqback/checkpoint-759.pt \
    --dims 512-512-512 \
    --latent_dims 256-256 \
    --use_latent_flow


