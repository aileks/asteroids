import math
import random

import pygame

from asteroids.circleshape import CircleShape
from asteroids.constants import (
    ASTEROID_MIN_RADIUS,
    LINE_WIDTH,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)
from asteroids.logger import log_event


class Asteroid(CircleShape):
    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, radius)
        # Generate lumpy shape points
        num_points = random.randint(8, 12)
        self.shape_points = []
        for i in range(num_points):
            angle = (360 / num_points) * i
            # Vary radius by up to 20%
            offset = random.uniform(0.8, 1.2)
            point_radius = radius * offset
            self.shape_points.append((angle, point_radius))

    def draw(self, screen: pygame.Surface) -> None:
        # Draw lumpy asteroid
        points = []
        for angle, point_radius in self.shape_points:
            rad = math.radians(angle)
            x = self.position.x + point_radius * math.cos(rad)
            y = self.position.y + point_radius * math.sin(rad)
            points.append((x, y))
        if len(points) > 2:
            pygame.draw.polygon(screen, "white", points, LINE_WIDTH)

    def update(self, dt: float) -> None:
        self.position += self.velocity * dt
        # Wrap around screen
        if self.position.x < -self.radius:
            self.position.x = SCREEN_WIDTH + self.radius
        elif self.position.x > SCREEN_WIDTH + self.radius:
            self.position.x = -self.radius
        if self.position.y < -self.radius:
            self.position.y = SCREEN_HEIGHT + self.radius
        elif self.position.y > SCREEN_HEIGHT + self.radius:
            self.position.y = -self.radius

    def split(self) -> None:
        self.kill()

        if self.radius <= ASTEROID_MIN_RADIUS:
            return

        log_event("asteroid_split")

        random_angle = random.uniform(20, 50)
        a = self.velocity.rotate(random_angle)
        b = self.velocity.rotate(-random_angle)

        new_radius = self.radius - ASTEROID_MIN_RADIUS
        asteroid = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid.velocity = a * 1.2
        asteroid = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid.velocity = b * 1.2
