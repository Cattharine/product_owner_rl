import datetime

def train():
    return [1, 2, 3]


if __name__ == '__main__':
    guidance = True
    rewards_log = train()
    now = datetime.datetime.now().strftime("%Y-%m-%d-T-%H-%M-%S")
    filename = f'guidance_{guidance}_rewards_{now}.txt'
    with open(filename, 'w') as file:
        print(rewards_log, file=file)