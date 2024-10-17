# Specialization to my personal workstation paths

# config for training GPT-2 (124M) down to very nice loss of ~2.85 on 1 node of 8X A100 40GB
# launch as the following (e.g. in a screen session) and wait ~5 days:
# $ torchrun --standalone --nproc_per_node=8 train.py config/train_gpt2.py

# These variables determine if the baseline gpt or the normalized gpt implementation will be executed
from gpt_model import GPT, GPTConfig
model_class = GPT
model_config = GPTConfig

experiment_name = wandb_run_name = 'base_gpt_test_run_pytorch_flash_attn'
out_dir = f"/results/{experiment_name}"

wandb_log = True
wandb_notes = """Baseline GPT implementation using pytorch's flash attention"""
wandb_project = "normalized_gpt_dev_sakle"
data_root_path='/data/'
dataset = 'nanoGPTopenwebtext'

# these make the total batch size be ~0.5M
# 12 batch size * 1024 block size * 5 gradaccum * 8 GPUs = 491,520
batch_size = 8
block_size = 1024
gradient_accumulation_steps = 64  # This gets downscaled by the number of gpus automatically in train.py
base_scale_override = None # set to None to default to normalized GPT initialization

compile = True
# this makes total number of tokens be 300B
max_iters = 600000
lr_decay_iters = 600000
learning_rate = 15e-4
grad_clip = 0.0 # clip gradients at this value, or disable if == 0.0
min_lr = 0.0
weight_decay = 0.1
warmup_iters = 2000

# Model dimension settings
n_layer = 12
n_head = 16
n_embd = 1024
base_scale_override = 1.0 / n_embd ** 0.5




