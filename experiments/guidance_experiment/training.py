import datetime
import os
import sys

sys.path.append('..')
sys.path.append('../..')

from environment import ProductOwnerEnv
from algorithms import DoubleDQN
from environment.reward_sytem.full_potential_credit_reward_system import (
    FullPotentialCreditRewardSystem,
)
from pipeline.aggregator_study import update_reward_system_config
from pipeline.metrics_study import MetricsStudy


def play_forward_with_empty_sprints(env: ProductOwnerEnv):
    info = env.get_info()
    done = env.get_done(info)
    total_reward = 0
    while not done:
        state, reward, done, info = env.step(0)
        total_reward += reward
    return total_reward


def train(guidance: bool):
    userstory_env = None
    backlog_env = None
    reward_system = FullPotentialCreditRewardSystem(config={})
    env = ProductOwnerEnv(userstory_env, backlog_env, guidance, reward_system)
    update_reward_system_config(env, reward_system)

    epsilon_decrease = 1e-5
    agent = DoubleDQN(env.state_dim, env.action_n, epsilon_decrease=epsilon_decrease)

    study = MetricsStudy(env, agent, 100)
    study.study_agent(10000)

    return study.rewards_log


if __name__ == "__main__":
    guidance = True
    rewards_log = train(guidance)
    now = datetime.datetime.now().strftime("%Y-%m-%d-T-%H-%M-%S")
    current_dir = os.getcwd()
    if "experiments" not in current_dir:
        current_dir = os.path.join(current_dir, "experiments", "guidance_experiment")
    filename = os.path.join(current_dir, f"guidance_{guidance}_rewards_{now}.txt")
    with open(filename, "w") as file:
        print(rewards_log, file=file)
