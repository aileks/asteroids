import random

import pygame

from asteroids.circleshape import CircleShape
from asteroids.constants import (
    LINE_WIDTH,
    POWERUP_DURATION,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    SHIELD_DURATION,
)


class PowerUp(CircleShape):
    POWERUP_TYPES = ["shield", "speed", "rapid_fire", "triple_shot"]

    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y, 15)
        self.powerup_type = random.choice(self.POWERUP_TYPES)
        self.rotation = 0.0
        self.rotation_speed = 90.0

    def draw(self, screen: pygame.Surface) -> None:
        # Draw power-up as a rotating diamond/square
        points = []
        for i in range(4):
            angle = self.rotation + i * 90
            point = self.position + pygame.Vector2(0, self.radius).rotate(angle)
            points.append(point)

        # Color based on type
        colors = {
            "shield": (0, 150, 255),  # Blue
            "speed": (255, 200, 0),  # Yellow
            "rapid_fire": (255, 0, 0),  # Red
            "triple_shot": (0, 255, 0),  # Green
        }
        color = colors.get(self.powerup_type, "white")
        pygame.draw.polygon(screen, color, points, LINE_WIDTH)

    def update(self, dt: float) -> None:
        self.rotation += self.rotation_speed * dt
        # Wrap around screen
        if self.position.x < 0:
            self.position.x = SCREEN_WIDTH
        elif self.position.x > SCREEN_WIDTH:
            self.position.x = 0
        if self.position.y < 0:
            self.position.y = SCREEN_HEIGHT
        elif self.position.y > SCREEN_HEIGHT:
            self.position.y = 0


class PowerUpManager:
    def __init__(self) -> None:
        self.shield_active = False
        self.shield_timer = 0.0
        self.speed_boost_active = False
        self.speed_boost_timer = 0.0
        self.rapid_fire_active = False
        self.rapid_fire_timer = 0.0
        self.triple_shot_active = False
        self.triple_shot_timer = 0.0

    def activate(self, powerup_type: str) -> None:
        if powerup_type == "shield":
            self.shield_active = True
            self.shield_timer = SHIELD_DURATION
        elif powerup_type == "speed":
            self.speed_boost_active = True
            self.speed_boost_timer = POWERUP_DURATION
        elif powerup_type == "rapid_fire":
            self.rapid_fire_active = True
            self.rapid_fire_timer = POWERUP_DURATION
        elif powerup_type == "triple_shot":
            self.triple_shot_active = True
            self.triple_shot_timer = POWERUP_DURATION

    def update(self, dt: float) -> None:
        if self.shield_active:
            self.shield_timer -= dt
            if self.shield_timer <= 0:
                self.shield_active = False

        if self.speed_boost_active:
            self.speed_boost_timer -= dt
            if self.speed_boost_timer <= 0:
                self.speed_boost_active = False

        if self.rapid_fire_active:
            self.rapid_fire_timer -= dt
            if self.rapid_fire_timer <= 0:
                self.rapid_fire_active = False

        if self.triple_shot_active:
            self.triple_shot_timer -= dt
            if self.triple_shot_timer <= 0:
                self.triple_shot_active = False
