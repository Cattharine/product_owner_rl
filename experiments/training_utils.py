import datetime
import os
import sys

import pandas as pd

from typing import List

sys.path.append("..")

from environment import CreditPayerEnv
from pipeline import LoggingStudy


def play_forward_with_empty_sprints(env: CreditPayerEnv):
    info = env.get_info()
    done = env.get_done(info)
    total_reward = 0
    context = env.game.context
    while not context.done and context.customers > 0:
        state, reward, done, info = env.step(0)
        total_reward += reward
    if context.customers <= 0:
        context.done = True
        context.is_loss = True


def eval_agent(study: LoggingStudy):
    study.agent.eval()
    state = study.env.reset()
    info = study.env.get_info()
    reward, _ = study.play_trajectory(state, info)
    play_forward_with_empty_sprints(study.env)
    game_context = study.env.game.context
    is_win = game_context.is_victory
    sprint = game_context.current_sprint
    return reward, is_win, sprint


def update_data_frame(path: str, df: pd.DataFrame):
    if os.path.exists(path):
        data = pd.read_csv(path)
    else:
        data = pd.DataFrame()

    data: pd.DataFrame = pd.concat([data, df])
    data.to_csv(path, index=False, float_format='%.5f')


def save_rewards(episode_n: int, rewards_log: List[float], now: str, flag: bool):
    df = pd.DataFrame(
        {
            "Trajectory": list(range(episode_n)),
            "Reward": rewards_log,
        }
    )
    df["DateTime"] = now
    df["Flag"] = flag
    rewards_path = "train_rewards.csv"
    update_data_frame(rewards_path, df)


def save_evaluation(evaluations: List, now: str, flag: bool):
    df = pd.DataFrame(evaluations, columns=["Reward", "Win", "Sprint"])
    df["DateTime"] = now
    df["Flag"] = flag
    evaluations_path = "evaluations.csv"
    update_data_frame(evaluations_path, df)
