import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from typing import List


def main():
    evals_df = pd.read_csv("evaluations.csv")
    print(evals_df.head())

    evals_grups = evals_df.groupby(["Flag", "DateTime"])

    grouped_wins = evals_grups["Win"].sum()
    print(grouped_wins)

    rewards_df = pd.read_csv("train_rewards.csv")
    reward_groups = rewards_df.groupby(["Flag", "Trajectory"])["Reward"]
    mean_rewards = reward_groups.mean().reset_index()
    new_reward = mean_rewards[mean_rewards["Flag"]]
    default_rewards = mean_rewards[~mean_rewards["Flag"]]

    plt.plot(new_reward["Trajectory"], new_reward["Reward"], label="Potential")
    plt.plot(default_rewards["Trajectory"], default_rewards["Reward"], label="Default")
    plt.legend()
    plt.title("Rewards")
    plt.xlabel("trajectory")
    plt.ylabel("rewards")
    plt.savefig("potential_rewards.png")
    plt.show()


if __name__ == "__main__":
    main()
