import os
import matplotlib.pyplot as plt
from typing import List


def get_experiment_files(filenames: List[str], guidance: bool):
    experiment_files = []
    prefix = f"guidance_{guidance}"
    for filename in filenames:
        if filename.startswith(prefix):
            experiment_files.append(filename)
    return experiment_files


def main():
    current_dir = os.getcwd()
    content = os.listdir(current_dir)

    data_files = []
    for filename in content:
        if filename.startswith("guidance"):
            data_files.append(filename)

    reward_files = []
    evaluation_files = []
    for data_file in data_files:
        if "rewards" in data_file:
            reward_files.append(data_file)
        if "evals" in data_file:
            evaluation_files.append(data_file)

    with open(reward_files[0], "r") as file:
        data = file.read()

    guidance_rewards = []
    guidance_rewards_files = get_experiment_files(reward_files, True)
    for filename in guidance_rewards_files:
        with open(filename, 'r') as file:
            data = eval(file.read())
            guidance_rewards.append(data)

    for rewards in guidance_rewards:
        plt.plot(rewards)
    plt.show()


if __name__ == "__main__":
    main()
