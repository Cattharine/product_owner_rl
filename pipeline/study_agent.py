import torch
from algorithms.deep_q_networks import DQN
from environment.environment import ProductOwnerEnv

from typing import List



class ConfidenceStudy:
    def __init__(self, env: ProductOwnerEnv, agent_generator, trajecory_max_len, repeat_count) -> None:
        self.rewards_logs: List[List[int]] = []
        self.q_value_logs: List[List[int]] = []


def save_dqn_agent(agent: DQN, path):
    torch.save(agent, path)


def load_dqn_agent(path):
    agent: DQN = torch.load(path)
    agent.eval()
    return agent
