from gym.envs.registration import register

register(
    id='nine-mens-morris-v0',
    entry_point='gym_nine_mens_morris.envs:NineMensMorrisEnv',
)
