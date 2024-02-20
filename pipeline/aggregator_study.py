from pipeline.logging_study import LoggingStudy
from environment import TutorialSolverEnv, CreditPayerEnv, ProductOwnerEnv
from environment.credit_payer_env import USUAL_CREDIT_ENV_END_SPRINT, EARLY_CREDIT_ENV_END_SPRINT


class AggregatorStudy(LoggingStudy):
    def __init__(self, env, agents, trajectory_max_len, save_rate=100) -> None:
        assert 0 < len(agents) < 5
        self.stage = len(agents)
        if self.stage == 1:
            assert isinstance(env, TutorialSolverEnv)
        if self.stage == 2:
            assert isinstance(env, CreditPayerEnv)
        if self.stage == 3:
            assert isinstance(env, CreditPayerEnv) and env.with_end
        if self.stage == 4:
            assert isinstance(env, ProductOwnerEnv)

        self.agents = agents
        super().__init__(env, agents[-1], trajectory_max_len, save_rate)

    def play_trajectory(self, state):
        full_reward = 0
        if self.stage > 1:
            state, reward, failed = self.play_tutorial(self.agents[0])
            full_reward += reward
            if failed:
                return reward
        if self.stage > 2:
            state, credit_reward, failed = self.play_credit_payment(self.agents[1], False)
            full_reward += credit_reward
            if failed:
                return full_reward
        if self.stage > 3:
            state, credit_reward, failed = self.play_credit_payment(self.agents[2], True)
            full_reward += credit_reward
            if failed:
                return full_reward
        full_reward += super().play_trajectory(state)
        print(f"full total_reward: {full_reward}")
        return full_reward

    def play_tutorial(self, tutorial_agent):
        env = TutorialSolverEnv(with_sprint=self.env.with_sprint)
        done = not self.env.game.context.is_new_game

        return self.play_some_stage(tutorial_agent, env, done, "tutorial")

    def play_credit_payment(self, credit_agent, with_end):
        env = CreditPayerEnv(with_sprint=self.env.with_sprint, with_end=with_end)
        end_sprint = USUAL_CREDIT_ENV_END_SPRINT if with_end else EARLY_CREDIT_ENV_END_SPRINT
        done = self.env.game.context.current_sprint == end_sprint

        return self.play_some_stage(credit_agent, env, done, "credit")

    def play_some_stage(self, agent, translator_env, init_done, name):
        agent.epsilon = 0
        translator_env.game = self.env.game
        done = init_done
        state = translator_env._get_state()
        inner_sprint_action_count = 0
        total_reward = 0

        while not done:
            action, inner_sprint_action_count = self._choose_action(agent, state,
                                                                    inner_sprint_action_count)
            state, reward, done, _ = translator_env.step(action)

            total_reward += reward

        print(f"{name} end")
        if translator_env.game.context.get_money() < 0:
            print(f"{name} failed")

        return self.env._get_state(), total_reward, translator_env.game.context.get_money() < 0
