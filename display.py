import gymnasium as gym
from config.config import Config
import argparse
import numpy as np
import torch

import logging
from logger.logger import Logger
from utils.tools import *

import time
import sys, os
sys.path.append(".")

from runner.multi_evo_agent_runner import MultiEvoAgentRunner
from runner.multi_agent_runner import MultiAgentRunner
from runner.selfplay_agent_runner import SPAgentRunner


def main():
    # ----------------------------------------------------------------------------#
    # Load config options from terminal and predefined yaml file
    # ----------------------------------------------------------------------------#
    parser = argparse.ArgumentParser(description="User's arguments from terminal.")
    parser.add_argument("--cfg", 
                        dest="cfg", 
                        help="run directory and cfg", 
                        required=True, 
                        type=str)
    parser.add_argument('--ckpt_dir', type=str, default=None)
    parser.add_argument('--ckpt', type=str, default='best')
    parser.add_argument('--symmetric', type=str2bool, default=True)
    parser.add_argument('--gpu_index', type=int, default=-1)
    parser.add_argument('--num_episode', type=int, default=1)
    args = parser.parse_args()
    # Load config file
    args.run_dir = os.path.split(args.cfg)[0] + '/'
    cfg_file = args.cfg
    cfg = Config(cfg_file)
    cfg.symmetric = args.symmetric

    # ----------------------------------------------------------------------------#
    # Define logger and create dirs
    # ----------------------------------------------------------------------------#
    # set logger
    logger = Logger(name='current', args=args, cfg=cfg)
    logger.propagate = False
    logger.setLevel(logging.INFO)
    # set output
    logger.set_output_handler()
    logger.print_system_info()
    # only training generates log file
    logger.critical('Type of current running: Evaluation. No log file will be created')
    # redefine dir
    logger.run_dir = args.run_dir
    logger.model_dir = '%smodels' % logger.run_dir
    logger.log_dir = '%slog' % logger.run_dir
    logger.tb_dir = '%stb' % logger.run_dir

    ckpt = [int(args.ckpt) if args.ckpt.isdigit() else args.ckpt] * 2

    # ----------------------------------------------------------------------------#
    # Set torch and random seed
    # ----------------------------------------------------------------------------#
    dtype = torch.float64
    torch.set_default_dtype(dtype)
    if args.gpu_index == -1:
        device = torch.device('cpu')
    else:
        device = torch.device('cuda', index=args.gpu_index) 
        if torch.cuda.is_available():
            torch.cuda.set_device(args.gpu_index)
        # np.random.seed(cfg.seed)
    # torch.manual_seed(cfg.seed)
    
    # ----------------------------------------------------------------------------#
    # Evaluation
    # ----------------------------------------------------------------------------#
    # runner definition
    # runner = MultiEvoAgentRunner(cfg, logger, dtype, device, 
    #                              num_threads=args.num_threads, training=False)

    torch.set_num_threads(1)

    if cfg.runner_type == "multi-agent-runner":
        runner = MultiAgentRunner(cfg, logger, dtype, device, training=False, ckpt_dir=args.ckpt_dir, ckpt=ckpt)
    elif cfg.runner_type == "selfplay-agent-runner":
        runner = SPAgentRunner(cfg, logger, dtype, device, training=False, ckpt_dir=args.ckpt_dir, ckpt=ckpt)
    elif cfg.runner_type == "multi-evo-agent-runner":
        runner = MultiEvoAgentRunner(cfg, logger, dtype, device, training=False, ckpt_dir=args.ckpt_dir, ckpt=ckpt)
    
    runner.display(num_episode=args.num_episode, mean_action=False, ckpt_dir=args.ckpt_dir)

if __name__ == "__main__":
    main()

