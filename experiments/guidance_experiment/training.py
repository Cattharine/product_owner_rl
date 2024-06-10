import datetime
import os
import sys

sys.path.append("..")
sys.path.append("../..")

from environment import CreditPayerEnv
from environment.backlog_env import BacklogEnv
from environment.userstory_env import UserstoryEnv
from environment.reward_sytem import EmpiricalCreditStageRewardSystem
from pipeline.aggregator_study import update_reward_system_config
from pipeline import LoggingStudy, CREDIT_END, CREDIT_START
from main import create_usual_agent


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
    is_loss = game_context.is_loss
    return reward, is_win, is_loss  # sprint


def parse_state_from_stage(stage):
    with_end = stage != CREDIT_START
    with_late_purchases_penalty = stage == CREDIT_END
    return with_end, with_late_purchases_penalty


def make_credit_study(trajectory_max_len, episode_n, with_info):
    userstory_env = UserstoryEnv(2, 0, 0)
    backlog_env = BacklogEnv(6, 0, 0, 0, 0, 0)
    reward_system = EmpiricalCreditStageRewardSystem(True, config={})
    env = CreditPayerEnv(
        userstory_env,
        backlog_env,
        with_end=True,
        with_info=with_info,
        reward_system=reward_system,
    )
    update_reward_system_config(env, reward_system)

    agent = create_usual_agent(env, trajectory_max_len, episode_n)

    study = LoggingStudy(env, agent, trajectory_max_len)
    study.study_agent(episode_n)

    return study


def main(guidance):
    study = make_credit_study(200, 1000, guidance)
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

if __name__ == "__main__":
    for i in range(5):
        main(False)