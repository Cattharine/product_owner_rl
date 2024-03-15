from environment import CreditPayerEnv
from pipeline import AggregatorStudy
from pipeline.study_agent import load_dqn_agent
from main import make_average_agent

import visualizer

def make_credit_start_study(tutorial_agent, trajectory_max_len, episode_n):
    env = CreditPayerEnv()

    agent = make_average_agent(env, trajectory_max_len, episode_n)

    agents = [tutorial_agent, agent]
    study = AggregatorStudy(env, agents, trajectory_max_len)

    study.study_agent(episode_n)

    return study

def main():
    tutorial_model_path = 'models/tutorial_model.pt'
    tutorial_agent = load_dqn_agent(tutorial_model_path)

    study = make_credit_start_study(tutorial_agent, 100, 40)

    visualizer.show_rewards(study, show_estimates=True, filename='figures/rewards.png')
    visualizer.show_sprints(study, filename='figures/sprints.png')
    visualizer.show_loss(study, filename='figures/loss.png')

if __name__ == '__main__':
    main()
