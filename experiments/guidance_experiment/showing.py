import os
import matplotlib.pyplot as plt


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

    plt.plot(eval(data))
    plt.show()


if __name__ == "__main__":
    main()
