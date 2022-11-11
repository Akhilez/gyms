import pandas as pd


class DragonStats:
    """
    One timestep = n frames.
    So we collect data for n frames, then aggregate it into one timestep stat and destroy the stats for n frames.

    Saving stats for every frame with keys:
    - frame number
    - timestep
    - action
    - health
    - has burnt animal
    - has burnt crossbow
    - has killed animal
    - has destroyed crossbow
    - has eaten animal
    - has acquired key
    - has unlocked
    - has flown away

    The keys for timestep will be:
    - timestep
    - first action
    - health begin
    - health end
    - n burnt animal
    - n burnt crossbow
    - n killed animal
    - n destroyed crossbow
    - n eaten animal
    - n acquired key
    - n unlocked
    - n flown away
    """
    def __init__(self, dragon):
        self.game = dragon.game
        self.dragon = dragon
        self.frame_stats = {}
        self.timestep_stats = {}

        # Frame stats
        self.has_burnt_animal = False
        self.has_burnt_crossbow = False
        self.has_killed_animal = False
        self.has_destroyed_crossbow = False
        self.has_eaten_animal = False
        self.has_acquired_key = False
        self.has_unlocked = False
        self.has_flown_away = False

    def step(
        self,
        action,
    ):
        self.frame_stats[self.game.episode_manager.frame] = {
            'timestep': self.game.episode_manager.timestep,
            'action': action,
            'health': self.dragon.health,
            'has_burnt_animal': self.has_burnt_animal,
            'has_burnt_crossbow': self.has_burnt_crossbow,
            'has_killed_animal': self.has_killed_animal,
            'has_destroyed_crossbow': self.has_destroyed_crossbow,
            'has_eaten_animal': self.has_eaten_animal,
            'has_acquired_key': self.has_acquired_key,
            'has_unlocked': self.has_unlocked,
            'has_flown_away': self.has_flown_away,
        }

        # Aggregate if new timestep
        if self.game.episode_manager.is_new_timestep():
            df = pd.DataFrame.from_dict(self.frame_stats, orient='index')
            self.timestep_stats[self.game.episode_manager.timestep] = {
                'first_action': df.iloc[0]['action'],
                'health_begin': df.iloc[0]['health'],
                'health_end': df.iloc[-1]['health'],
                'n_burnt_animal': df.has_burnt_animal.sum(),
                'n_burnt_crossbow': df.has_burnt_crossbow.sum(),
                'n_killed_animal': df.has_killed_animal.sum(),
                'n_destroyed_crossbow': df.has_destroyed_crossbow.sum(),
                'n_eaten_animal': df.has_eaten_animal.sum(),
                'n_acquired_key': df.has_acquired_key.sum(),
                'n_unlocked': df.has_unlocked.sum(),
                'n_flown_away': df.has_flown_away.sum(),
            }
            self.frame_stats = {}

        # Reset flags
        self.has_burnt_animal = False
        self.has_burnt_crossbow = False
        self.has_killed_animal = False
        self.has_destroyed_crossbow = False
        self.has_eaten_animal = False
        self.has_acquired_key = False
        self.has_unlocked = False
        self.has_flown_away = False

    def get_reward(self):
        stats = self.timestep_stats[self.game.episode_manager.timestep]
        reward = 0.0
        for key in self.game.params.stats.reward_map.__fields__.keys():
            if stats[f'n_{key}'] > 0:
                reward += getattr(self.game.params.stats.reward_map, key)
        return reward

    def get_stats(self):
        df = pd.DataFrame.from_dict(self.timestep_stats, orient='index')
        return df
