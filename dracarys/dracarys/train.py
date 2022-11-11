from os import makedirs
from os.path import join
import stable_baselines3
from stable_baselines3.common.env_checker import check_env
import pandas as pd
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.vec_env import (
    DummyVecEnv,
    VecFrameStack,
    VecVideoRecorder,
)
from dracarys.constants import BASE_DIR
from dracarys.env import DracarysEnv

# nohup python train.py > /dev/null 2>&1 &

exp = "framestack2"
output_dir = join(BASE_DIR, "temp", "models", exp)
makedirs(output_dir, exist_ok=True)

# ------------ ENV --------------

# env = DracarysEnv()
# check_env(env)
# print(env.observation_space.shape, env.action_space)

env = DummyVecEnv([lambda: Monitor(DracarysEnv())])
env = VecVideoRecorder(
    env,
    video_folder=join(output_dir, "videos"),
    record_video_trigger=lambda steps: steps % 5000 == 0,
    video_length=500,
    name_prefix=exp,
)
env = VecFrameStack(env, n_stack=3)

# ---------- MODEL --------------
model = stable_baselines3.PPO(
    "CnnPolicy",
    env,
    verbose=1,
    tensorboard_log=join(BASE_DIR, "tensorboard_log"),
    # exploration_final_eps=0.1,
    # exploration_fraction=0.3,
    device="cuda:1",
)

model.load(join(BASE_DIR, 'temp', 'models', 'framestack', 'model_framestack'), device='cuda:1')
model.learn(total_timesteps=1_000_000)
model.save(join(output_dir, f'model_{exp}'))

# --------------- ROLLOUT --------------

dfs = []
for j in range(3):
    print(f'Rollout {j}')
    obs = env.reset()
    for i in range(1_000):
        df = env.unwrapped.envs[0].game.objects_manager.dragons[0].stats.get_stats()
        action, _states = model.predict(obs, deterministic=True)
        # action = env.action_space.sample()
        try:
            obs, rewards, dones, info = env.step([int(action)])
        except:
            pass
        # print(rewards, dones, obs.shape)
        if dones[0]:
            break
    dfs.append(df)

df = pd.concat(dfs)
df.to_csv(join(output_dir, f"stats_{exp}.csv"))
