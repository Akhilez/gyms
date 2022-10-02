from gym.envs.registration import register
from sryvl.envs.sryvl_v0.env import SrYvlLvl0Env

register(
    id='sryvl-v0',
    entry_point='sryvl.envs.sryvl_v0.env:SrYvlLvl0Env',
)
