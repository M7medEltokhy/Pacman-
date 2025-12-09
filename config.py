import pygame

# ---------- إعدادات عامة ----------
WIDTH, HEIGHT = 800, 600
FPS = 60

# ألوان
BG_COLOR = (10, 10, 30)
PACMAN_COLOR = (255, 205, 0)
EYE_COLOR = (0, 0, 0)
PELLET_COLOR = (255, 200, 200)
HUD_COLOR = (230, 230, 230)
GHOST_COLORS = [(255, 0, 0), (255, 128, 255), (0, 255, 255), (255, 165, 0)]

# باك-مان افتراضيات
start_pos = [WIDTH // 4, HEIGHT // 2]
radius = 28
base_speed = 3.2

# فم باك-مان
mouth_open = 0.0
mouth_target = 0.0
mouth_speed_param = 6.0
mouth_max_angle = 35

# إعداد Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pacman")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 28)
large_font = pygame.font.SysFont(None, 56)
