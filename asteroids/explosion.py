import random

import pygame

from asteroids.circleshape import CircleShape
from asteroids.constants import EXPLOSION_DURATION, EXPLOSION_PARTICLES


class ExplosionParticle(CircleShape):
    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y, 3)
        angle = random.uniform(0, 360)
        speed = random.uniform(50, 150)
        self.velocity = pygame.Vector2(0, 1).rotate(angle) * speed
        self.lifetime = EXPLOSION_DURATION
        self.max_lifetime = EXPLOSION_DURATION

    def draw(self, screen: pygame.Surface) -> None:
        if self.lifetime > 0:
            alpha = int(255 * (self.lifetime / self.max_lifetime))
            color = (255, min(255, alpha + 100), 0)
            size = int(self.radius * (self.lifetime / self.max_lifetime))
            if size > 0:
                pygame.draw.circle(screen, color, self.position, size)

    def update(self, dt: float) -> None:
        self.position += self.velocity * dt
        self.velocity *= 0.98  # Friction
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.kill()


class Explosion:
    @staticmethod
    def create(x: float, y: float, containers: tuple) -> None:
        for _ in range(EXPLOSION_PARTICLES):
            particle = ExplosionParticle(x, y)
            if hasattr(particle, "containers"):
                particle.containers = containers  # type: ignore
            particle.add(containers)  # type: ignore
