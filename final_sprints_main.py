from pipeline.study_agent import load_dqn_agent


def main():
    tutorial_model_path = 'models/tutorial_model.pt'
    tutorial_agent = load_dqn_agent(tutorial_model_path)

    credit_start_path = 'models/credit_start_model.pt'
    credit_start_agent = load_dqn_agent(credit_start_path)

    credit_end_path = 'models/credit_end_model.pt'
    credit_end_agent = load_dqn_agent(credit_end_path)

    agents = [tutorial_agent, credit_start_agent, credit_end_agent]

if __name__ == '__main__':
    main()
