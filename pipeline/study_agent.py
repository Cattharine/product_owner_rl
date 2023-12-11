import os
import torch
import datetime
from algorithms.deep_q_networks import DQN

from typing import List


class BaseStudyDQN:
    def __init__(self, env, agent, trajecory_max_len) -> None:
        self.env = env
        self.agent: DQN = agent
        self.trajectory_max_len = trajecory_max_len

    def play_trajectory(self, init_state):
        total_reward = 0
        state = init_state
        for t in range(self.trajectory_max_len):
            action = self.agent.get_action(state)
            next_state, reward, done, _ = self.env.step(action)

            self.agent.fit(state, action, reward, done, next_state)

            state = next_state
            total_reward += reward

            if done:
                break
        
        return reward
    
    def study_agent(self, episode_n):
        for episode in range(episode_n):
            state = self.env.reset()
            self.play_trajectory(state)

class LoggingStudy(BaseStudyDQN):
    def __init__(self, env, agent, trajecory_max_len, save_rate=1000) -> None:
        super().__init__(env, agent, trajecory_max_len)
        self.episode = 0
        self.rewards_log: List[int] = []
        self.q_value_log: List[int] = []
        self.time_log: List[datetime.datetime] = []
        self.save_rate = save_rate
    
    def play_trajectory(self, init_state):
        with torch.no_grad():
            state = torch.tensor(init_state)
            q_values: torch.Tensor = self.agent.q_function(state)
            self.q_value_log.append(q_values.max())
        
        reward = super().play_trajectory(init_state)

        self.rewards_log.append(reward)

        print(f"episode: {self.episode}, total_reward: {reward}")
    
    def study_agent(self, episode_n):
        epoche_n = (episode_n + self.save_rate - 1) // self.save_rate

        os.makedirs('dqn', exist_ok=True)

        for epoche in range(epoche_n):
            path = f'dqn/model_{epoche}.pt'
            super().study_agent(self.save_rate)
            save_dqn_agent(self.agent, path=path)

def save_dqn_agent(agent: DQN, path):
    torch.save(agent, path)

def load_dqn_agent(path):
    agent = torch.load(path)
    agent.eval()
    return agent
