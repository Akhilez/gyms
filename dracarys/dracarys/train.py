from os.path import join
import stable_baselines3
from stable_baselines3.common.env_checker import check_env
from dracarys.constants import BASE_DIR
from dracarys.env import DracarysEnv

env = DracarysEnv()

check_env(env)

print(env.observation_space.shape, env.action_space)

model = stable_baselines3.PPO (
    'CnnPolicy',
    env,
    verbose=1,
    tensorboard_log=join(BASE_DIR, 'tensorboard_log'),
    # exploration_final_eps=0.1,
    # exploration_fraction=0.3,
)

model.learn(total_timesteps=400_000)
