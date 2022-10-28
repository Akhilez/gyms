from gym.envs.registration import register

register(
    id='dracarys-v1',
    entry_point='dracarys.env:DracarysEnv',
)
