import pygame

from asteroids.circleshape import CircleShape
from asteroids.constants import (
    BOMB_RADIUS,
    LINE_WIDTH,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)


class Bomb(CircleShape):
    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y, BOMB_RADIUS)
        self.lifetime = 1.0  # Explodes after 1 second
        self.max_lifetime = 1.0
        self.exploded = False

    def draw(self, screen: pygame.Surface) -> None:
        # Draw bomb as a pulsing circle
        if not self.exploded:
            progress = 1.0 - (self.lifetime / self.max_lifetime)
            size = int(self.radius * progress)
            if size > 0:
                pygame.draw.circle(
                    screen, (255, 100, 0), self.position, size, LINE_WIDTH
                )
                pygame.draw.circle(
                    screen, (255, 200, 0), self.position, max(1, size // 2), LINE_WIDTH
                )

    def update(self, dt: float) -> None:
        if not self.exploded:
            self.lifetime -= dt
            if self.lifetime <= 0:
                self.exploded = True
            # Wrap around screen
            if self.position.x < 0:
                self.position.x = SCREEN_WIDTH
            elif self.position.x > SCREEN_WIDTH:
                self.position.x = 0
            if self.position.y < 0:
                self.position.y = SCREEN_HEIGHT
            elif self.position.y > SCREEN_HEIGHT:
                self.position.y = 0
