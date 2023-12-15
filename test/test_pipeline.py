from pipeline.study_agent import BaseStudyDQN
from algorithms.deep_q_networks import DQN
from environment.environment import ProductOwnerEnv
import unittest


class TestPipeline(unittest.TestCase):
    def setUp(self):
        self.env = ProductOwnerEnv()

        state_dim = self.env.state_dim
        action_n = self.env.action_n
        self.agent = DQN(state_dim, action_n)

        self.study = BaseStudyDQN(self.env, self.agent, 1_000)

    def test_run_study_should_not_raise(self):
        self.study.study_agent(1)
