import pygame
import sys
import math
from config import *
from gamestate import GameState
from pacman import draw_pacman

def game_over_screen(gs):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                elif event.key == pygame.K_ESCAPE:
                    return False

        screen.fill((5, 5, 30))
        over_text = large_font.render("GAME OVER", True, (220, 50, 50))
        score_text = font.render(f"Final Score: {gs.score}", True, HUD_COLOR)
        instruct = font.render("Press R to Restart or ESC to Quit", True, HUD_COLOR)

        screen.blit(over_text, over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50)))
        screen.blit(score_text, score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 6)))
        screen.blit(instruct, instruct.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 46)))
        pygame.display.flip()
        clock.tick(10)

def main():
    gs = GameState()
    running = True
    global mouth_open, mouth_target, mouth_speed_param

    show_level_message = True
    level_msg_timer = 1.2

    while running:
        dt = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        keys = pygame.key.get_pressed()
        vx, vy = 0.0, 0.0
        speed = base_speed + 0.12 * (gs.level - 1)
        if keys[pygame.K_LEFT]:
            vx = -speed
        elif keys[pygame.K_RIGHT]:
            vx = speed
        if keys[pygame.K_UP]:
            vy = -speed
        elif keys[pygame.K_DOWN]:
            vy = speed
        if vx != 0 or vy != 0:
            gs.vel = [vx, vy]

        t = pygame.time.get_ticks() / 1000.0
        mouth_target = (math.sin(t * math.pi * mouth_speed_param) + 1) / 2
        mouth_open += (mouth_target - mouth_open) * min(1.0, 8.0 * dt)
        current_mouth_angle = mouth_open * mouth_max_angle

        gs.pac_pos[0] += gs.vel[0] * dt * 60.0
        gs.pac_pos[1] += gs.vel[1] * dt * 60.0

        # حدود الشاشة
        if gs.pac_pos[0] - radius < 0:
            gs.pac_pos[0] = radius
        if gs.pac_pos[0] + radius > WIDTH:
            gs.pac_pos[0] = WIDTH - radius
        if gs.pac_pos[1] - radius < 0:
            gs.pac_pos[1] = radius
        if gs.pac_pos[1] + radius > HEIGHT:
            gs.pac_pos[1] = HEIGHT - radius

        # تحديث الأشباح
        for g in gs.ghosts:
            g.update(gs.pac_pos, dt, gs.level)

        # التصادم مع الحبات
        remaining = []
        for p in gs.pellets:
            if math.hypot(p[0] - gs.pac_pos[0], p[1] - gs.pac_pos[1]) <= (p[2] + radius * 0.6):
                gs.score += 10
            else:
                remaining.append(p)
        gs.pellets = remaining

        # إدارة مؤقتات الاصطدام والإحياء
        if gs.invulnerable_time > 0:
            gs.invulnerable_time -= dt

        if gs.respawn_timer > 0:
            gs.respawn_timer -= dt
            if gs.respawn_timer <= 0:
                gs.pac_pos = [float(start_pos[0]), float(start_pos[1])]
                gs.invulnerable_time = 0.6
        else:
            for g in gs.ghosts:
                if math.hypot(g.pos[0] - gs.pac_pos[0], g.pos[1] - gs.pac_pos[1]) < (g.radius + radius - 6):
                    if gs.invulnerable_time <= 0:
                        gs.lives -= 1
                        gs.invulnerable_time = 1.0
                        gs.respawn_timer = 1.2
                        if gs.lives <= 0:
                            restart = game_over_screen(gs)
                            if not restart:
                                pygame.quit()
                                sys.exit()
                            else:
                                gs = GameState()
                                show_level_message = True
                                level_msg_timer = 1.2
                                break
                    break

        # مستوى جديد
        if not gs.pellets and gs.respawn_timer <= 0:
            gs.level += 1
            gs.score += 500
            mouth_speed_param += 0.6
            gs.reset_level()
            show_level_message = True
            level_msg_timer = 1.4

        # رسم اللعبة
        screen.fill(BG_COLOR)

        for p in gs.pellets:
            pygame.draw.circle(screen, PELLET_COLOR, (int(p[0]), int(p[1])), p[2])

        for g in gs.ghosts:
            g.draw(screen)

        flash = 1.0
        if gs.invulnerable_time > 0:
            flash = 0.4 + 0.6 * (0.5 * (1 + math.sin(pygame.time.get_ticks() / 100.0)))

        dir_vec = gs.vel if (gs.vel[0] != 0 or gs.vel[1] != 0) else (1, 0)
        pac_surface = pygame.Surface((radius * 2 + 4, radius * 2 + 4), pygame.SRCALPHA)
        draw_pacman(pac_surface, (radius + 2, radius + 2), radius, dir_vec, current_mouth_angle, mouth_open)
        pac_surface.set_alpha(int(255 * flash))
        screen.blit(pac_surface, (int(gs.pac_pos[0] - radius - 2), int(gs.pac_pos[1] - radius - 2)))

        hud = f"Score: {gs.score}    Lives: {gs.lives}    Level: {gs.level}    Pellets: {len(gs.pellets)}"
        text = font.render(hud, True, HUD_COLOR)
        screen.blit(text, (12, 10))

        if show_level_message:
            level_text = large_font.render(f"Level {gs.level}", True, HUD_COLOR)
            rect = level_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(level_text, rect)
            level_msg_timer -= dt
            if level_msg_timer <= 0:
                show_level_message = False

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
