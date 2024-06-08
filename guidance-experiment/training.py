import datetime

from environment import ProductOwnerEnv

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
    reward_system = None
    env = ProductOwnerEnv(userstory_env, backlog_env, guidance, reward_system)
    
    agent = None
    return [1, 2, 3]


if __name__ == '__main__':
    guidance = True
    rewards_log = train(guidance)
    now = datetime.datetime.now().strftime("%Y-%m-%d-T-%H-%M-%S")
    filename = f'guidance_{guidance}_rewards_{now}.txt'
    with open(filename, 'w') as file:
        print(rewards_log, file=file)