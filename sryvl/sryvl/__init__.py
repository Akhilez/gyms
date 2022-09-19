from gym.envs.registration import register


register(
    id='sryvl-v0',
    entry_point='sryvl.envs.sryvl_v0.sryvl.SrYvlEnv',
)
