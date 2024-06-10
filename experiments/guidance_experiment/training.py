import datetime
import os
import sys

sys.path.append("..")
sys.path.append("../..")

from environment import ProductOwnerEnv
from environment.backlog_env import BacklogEnv
from environment.userstory_env import UserstoryEnv
from algorithms import DoubleDQN
from environment.reward_sytem import EmpiricalRewardSystem
from pipeline.aggregator_study import update_reward_system_config
from pipeline import MetricsStudy, LoggingStudy


def play_forward_with_empty_sprints(env: ProductOwnerEnv):
    info = env.get_info()
    done = env.get_done(info)
    total_reward = 0
    while not done:
        state, reward, done, info = env.step(0)
        total_reward += reward
    return total_reward


def eval_agent(study: MetricsStudy):
    study.agent.epsilon = 0
    study.agent.epsilon_min = 0
    state = study.env.reset()
    info = study.env.get_info()
    reward, _ = study.play_trajectory(state, info)
    game_context = study.env.game.context
    is_win = game_context.is_victory
    is_loss = game_context.is_loss
    return reward, is_win, is_loss


def train(guidance: bool):
    userstory_env = None
    backlog_env = None
    reward_system = EmpiricalRewardSystem(config={})
    env = ProductOwnerEnv(userstory_env, backlog_env, guidance, reward_system)
    update_reward_system_config(env, reward_system)

    epsilon_decrease = 1e-5
    agent = DoubleDQN(env.state_dim, env.action_n, epsilon_decrease=epsilon_decrease)

    study = LoggingStudy(env, agent, 200)
    study.study_agent(10000)

    return study


if __name__ == "__main__":
    guidance = True
    study = train(guidance)
    now = datetime.datetime.now().strftime("%Y-%m-%d-T-%H-%M-%S")
    current_dir = os.getcwd()
    if "experiments" not in current_dir:
        current_dir = os.path.join(current_dir, "experiments", "guidance_experiment")
    filename = os.path.join(current_dir, f"guidance_{guidance}_rewards_{now}.txt")
    with open(filename, "w") as file:
        print(study.rewards_log, file=file)

    evaluations = []
    for i in range(100):
        evaluation = eval_agent(study)
        evaluations.append(evaluation)

    filename = os.path.join(current_dir, f"guidance_{guidance}_evals_{now}.txt")
    with open(filename, "w") as file:
        print(evaluations, file=file)
