import os
import matplotlib.pyplot as plt
import numpy as np
from typing import List


def get_experiment_files(filenames: List[str], guidance: bool):
    experiment_files = []
    prefix = f"guidance_{guidance}"
    for filename in filenames:
        if filename.startswith(prefix):
            experiment_files.append(filename)
    return experiment_files


def get_all_data_files(directory_path: str):
    content = os.listdir(directory_path)

    data_files = []
    for filename in content:
        if filename.startswith("guidance"):
            data_files.append(filename)
    return data_files


def read_files_data(filenames: List[str]):
    result = []
    for filename in filenames:
        with open(filename, "r") as file:
            data = eval(file.read())
            result.append(data)
    return result


def main():
    current_dir = os.getcwd()

    data_files = get_all_data_files(current_dir)

    reward_files = []
    evaluation_files = []
    for data_file in data_files:
        if "rewards" in data_file:
            reward_files.append(data_file)
        if "evals" in data_file:
            evaluation_files.append(data_file)

    guidance_rewards_files = get_experiment_files(reward_files, True)
    guidance_rewards = read_files_data(guidance_rewards_files)
    rewards = np.array(guidance_rewards)

    default_rewards_files = get_experiment_files(reward_files, False)
    default_rewards = read_files_data(default_rewards_files)

    # plt.plot(rewards.mean(axis=0), ".", label="Guidance mean result")
    # plt.plot(np.mean(default_rewards, axis=0), ".", label="Deafault mean rewards")
    # plt.plot(np.median(rewards, axis=0), ".")
    # plt.show()

    guidance_evaluation_files = get_experiment_files(evaluation_files, True)
    guidance_evaluation = read_files_data(guidance_evaluation_files)
    guidance_evaluation = np.array(guidance_evaluation)
    wins = guidance_evaluation[:, :, 1]
    print(wins)
    print(wins.sum(axis=1))


if __name__ == "__main__":
    main()
