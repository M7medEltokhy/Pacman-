from pellets import make_pellets
from ghosts import Ghost
from config import start_pos, base_speed, GHOST_COLORS, WIDTH, HEIGHT

import random
import math

class GameState:
    def __init__(self):
        self.level = 1
        self.score = 0
        self.lives = 3
        self.pac_pos = [float(start_pos[0]), float(start_pos[1])]
        self.vel = [base_speed, 0.0]
        self.pellets = make_pellets()
        self.ghosts = []
        self.respawn_timer = 0.0
        self.invulnerable_time = 0.0
        self.spawn_ghosts_for_level()

    def spawn_ghosts_for_level(self):
        self.ghosts.clear()
        num_ghosts = min(4, 1 + (self.level - 1))
        base_ghost_speed = 70 + 8 * (self.level - 1)
        for i in range(num_ghosts):
            tries = 0
            while True:
                x = random.randint(100, WIDTH - 100)
                y = random.randint(80, HEIGHT - 80)
                if math.hypot(x - self.pac_pos[0], y - self.pac_pos[1]) > 140:
                    break
                tries += 1
                if tries > 200:
                    break
            color = GHOST_COLORS[i % len(GHOST_COLORS)]
            g = Ghost(x, y, color, base_ghost_speed)
            self.ghosts.append(g)

    def reset_level(self):
        self.pellets = make_pellets()
        self.pac_pos = [float(start_pos[0]), float(start_pos[1])]
        self.vel = [base_speed, 0.0]
        self.invulnerable_time = 0.8
        self.spawn_ghosts_for_level()
