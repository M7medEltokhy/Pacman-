import pygame
import math
import random
from config import WIDTH, HEIGHT, GHOST_COLORS

class Ghost:
    def __init__(self, x, y, color, speed):
        self.pos = [float(x), float(y)]
        self.color = color
        self.speed = float(speed)
        vx = random.uniform(-1.0, 1.0)
        vy = random.uniform(-1.0, 1.0)
        vlen = math.hypot(vx, vy) + 1e-6
        self.dir = [vx / vlen, vy / vlen]
        self.frightened = False
        self.radius = 22

    def update(self, pac_pos, dt, level):
        chase_factor = 0.55 + 0.05 * level
        if random.random() < 0.02:
            self.dir = [random.uniform(-1, 1), random.uniform(-1, 1)]

        to_pac = [pac_pos[0] - self.pos[0], pac_pos[1] - self.pos[1]]
        dist = math.hypot(to_pac[0], to_pac[1]) + 1e-6
        to_pac_norm = [to_pac[0] / dist, to_pac[1] / dist]

        self.dir[0] = (1 - chase_factor) * self.dir[0] + chase_factor * to_pac_norm[0]
        self.dir[1] = (1 - chase_factor) * self.dir[1] + chase_factor * to_pac_norm[1]

        dlen = math.hypot(self.dir[0], self.dir[1]) + 1e-6
        self.dir[0] /= dlen
        self.dir[1] /= dlen

        self.pos[0] += self.dir[0] * self.speed * dt
        self.pos[1] += self.dir[1] * self.speed * dt

        if self.pos[0] - self.radius < 0:
            self.pos[0] = self.radius
            self.dir[0] *= -1
        if self.pos[0] + self.radius > WIDTH:
            self.pos[0] = WIDTH - self.radius
            self.dir[0] *= -1
        if self.pos[1] - self.radius < 0:
            self.pos[1] = self.radius
            self.dir[1] *= -1
        if self.pos[1] + self.radius > HEIGHT:
            self.pos[1] = HEIGHT - self.radius
            self.dir[1] *= -1

    def draw(self, surface):
        x, y = int(self.pos[0]), int(self.pos[1])
        pygame.draw.circle(surface, self.color, (x, y), self.radius)
        eye_offset = 10
        pygame.draw.circle(surface, (255, 255, 255), (x - eye_offset, y - 6), 6)
        pygame.draw.circle(surface, (255, 255, 255), (x + eye_offset, y - 6), 6)
        pygame.draw.circle(surface, (0, 0, 0), (x - eye_offset, y - 6), 3)
        pygame.draw.circle(surface, (0, 0, 0), (x + eye_offset, y - 6), 3)
