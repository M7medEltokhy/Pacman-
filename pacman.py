import pygame
import math
from config import PACMAN_COLOR, EYE_COLOR, BG_COLOR

def draw_pacman(surface, center, radius, direction_vector, mouth_angle_deg, mouth_open_ratio):
    cx, cy = center
    dx, dy = direction_vector
    if dx == 0 and dy == 0:
        dx = 1
    angle = math.degrees(math.atan2(-dy, dx))
    half_angle = mouth_angle_deg * mouth_open_ratio
    a1 = math.radians(angle + half_angle)
    a2 = math.radians(angle - half_angle)

    pygame.draw.circle(surface, PACMAN_COLOR, (int(cx), int(cy)), radius)

    mouth_points = [(cx, cy)]
    steps = 12
    for t in range(steps + 1):
        theta = a1 + (a2 - a1) * (t / steps)
        mouth_points.append((cx + radius * math.cos(theta), cy - radius * math.sin(theta)))

    try:
        pygame.draw.polygon(surface, (0, 0, 0, 0), mouth_points)
    except TypeError:
        pygame.draw.polygon(surface, BG_COLOR, mouth_points)

    eye_offset_angle = math.radians(angle - 25)
    eye_dist = radius * 0.45
    eye_x = cx + eye_dist * math.cos(eye_offset_angle)
    eye_y = cy - eye_dist * math.sin(eye_offset_angle)
    eye_radius = max(3, int(radius * 0.12))
    pygame.draw.circle(surface, EYE_COLOR, (int(eye_x), int(eye_y)), eye_radius)
