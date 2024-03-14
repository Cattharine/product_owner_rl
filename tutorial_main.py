from environment import TutorialSolverEnv
from algorithms import DoubleDQN
from pipeline import LoggingStudy

from pipeline.study_agent import save_dqn_agent

import visualizer

def make_tutorial_study(trajectory_max_len, episode_n):
    env = TutorialSolverEnv()

    state_dim = env.state_dim
    action_n = env.action_n

    epsilon_decrease = 1 / (trajectory_max_len * episode_n)
    agent = DoubleDQN(
            state_dim, action_n, gamma=0.9, tau=0.001, epsilon_decrease=epsilon_decrease
        )
    study = LoggingStudy(env, agent, trajectory_max_len)
    study.SAVE_MEMORY = False

    study.study_agent(episode_n)
    return study

def main():
    study = make_tutorial_study(trajectory_max_len=100, episode_n=40)
    agent = study.agent

    visualizer.show_rewards(study, show_estimates=True, filename='figures/rewards.png')
    visualizer.show_sprints(study, filename='figures/sprints.png')
    visualizer.show_loss(study, filename='figures/loss.png')

    agent.memory = []
    save_dqn_agent(agent, 'models/tutorial_model.pt')

if __name__ == "__main__":
    main()
