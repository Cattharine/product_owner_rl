import optuna

import numpy as np

from algorithms import DoubleDQN
from environment import CreditPayerEnv
from pipeline import MetricsStudy


def eval_trajectory(env: CreditPayerEnv, agent: DoubleDQN, trajectory_max_len: int):
    total_reward = 0
    state = env.reset()
    for i in range(trajectory_max_len):
        action = agent.get_action(state)

        state, reward, done, _ = env.step(action)

        total_reward += reward

        if done:
            break

    return total_reward


def eval_model(
    env: CreditPayerEnv, agent: DoubleDQN, trajectory_max_len: int, repeat_count: int
):
    rewards = []
    for i in range(repeat_count):
        reward = eval_trajectory(env, agent, trajectory_max_len)
        rewards.append(reward)

    return np.mean(rewards)


def double_objective(trial: optuna.Trial):
    env = CreditPayerEnv()
    state_dim = env.state_dim
    action_n = env.action_n

    trajectory_max_len = 100

    tau = trial.suggest_float("tau", 0.5, 0.99)

    agent = DoubleDQN(state_dim, action_n, tau=tau)
    study = MetricsStudy(env, agent, trajectory_max_len)

    study.study_agent(episode_n=50)

    agent.epsilon_min = 0
    agent.epsilon = 0

    return eval_model(env, agent, trajectory_max_len, repeat_count=10)


double_study = optuna.create_study(direction="maximize")
double_study.optimize(double_objective, n_trials=5)

trial = double_study.best_trial

print("Reward: {}".format(trial.value))
print("Best hyperparameters: {}".format(trial.params))

fig = optuna.visualization.plot_optimization_history(double_study)
fig.show()

fig = optuna.visualization.plot_slice(double_study)
fig.show()
