#! /bin/bash

python demo.py \
    --cates car \
    --resume_checkpoint checkpoints/gen/shapenet15k-catecar-seqback/checkpoint-latest.pt \
    --dims 512-512-512 \
    --latent_dims 256-256 \
    --use_latent_flow \
    --num_sample_shapes 20 \
    --num_sample_points 2048

