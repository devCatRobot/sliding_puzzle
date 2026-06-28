import math
import random

import pygame

FIREWORK_COLORS = [
    (255, 80, 80),
    (255, 200, 50),
    (80, 255, 120),
    (100, 180, 255),
    (255, 120, 255),
]


def create_firework(x, y):
    particles = []

    for _ in range(30):
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 6)
        particles.append(
            {
                "x": float(x),
                "y": float(y),
                "vx": math.cos(angle) * speed,
                "vy": math.sin(angle) * speed,
                "color": random.choice(FIREWORK_COLORS),
                "life": random.randint(40, 60),
            }
        )

    return particles


def draw_fireworks(screen, particles):
    for particle in particles:
        if particle["life"] <= 0:
            continue

        position = (int(particle["x"]), int(particle["y"]))
        radius = max(2, particle["life"] // 10)
        pygame.draw.circle(screen, particle["color"], position, radius)


def update_fireworks(particles):
    alive = []

    for particle in particles:
        particle["x"] += particle["vx"]
        particle["y"] += particle["vy"]
        particle["vy"] += 0.15
        particle["life"] -= 1

        if particle["life"] > 0:
            alive.append(particle)

    return alive


def tick_fireworks(fireworks, win_frames, window_width, window_height):
    win_frames += 1
    if win_frames % 45 == 0:
        x = random.randint(50, window_width - 50)
        y = random.randint(50, window_height - 50)
        fireworks.extend(create_firework(x, y))
    return update_fireworks(fireworks), win_frames
