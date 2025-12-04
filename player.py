from typing import Optional

import pygame
from bomb import Bomb
from circleshape import CircleShape
from shot import Shot
from constants import (
    BOMB_COOLDOWN,
    LINE_WIDTH,
    PLAYER_ACCELERATION,
    PLAYER_FRICTION,
    PLAYER_MAX_SPEED,
    PLAYER_RADIUS,
    PLAYER_SHOOT_COOLDOWN_SECONDS,
    PLAYER_SHOOT_SPEED,
    PLAYER_TURN_SPEED,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    SPEED_BOOST_MULTIPLIER,
)


class Player(CircleShape):
    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation: float = 0
        self.shoot_timer: float = 0
        self.bomb_timer: float = 0
        self.weapon_type: str = "normal"  # normal, rapid_fire, triple_shot
        self.speed_boost_active: bool = False
        self.shield_active: bool = False

    def triangle(self) -> list[pygame.Vector2]:
        forward: pygame.Vector2 = pygame.Vector2(0, 1).rotate(self.rotation)
        right: pygame.Vector2 = (
            pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        )
        a: pygame.Vector2 = self.position + forward * self.radius
        b: pygame.Vector2 = self.position - forward * self.radius - right
        c: pygame.Vector2 = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen: pygame.Surface) -> None:
        color = "cyan" if self.shield_active else "white"
        pygame.draw.polygon(screen, color, self.triangle(), LINE_WIDTH)  # type: ignore
        if self.shield_active:
            # Draw shield effect
            pygame.draw.circle(
                screen, (0, 150, 255, 100), self.position, self.radius + 5, 2
            )

    def rotate(self, dt: float) -> None:
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt: float) -> None:
        unit_vector: pygame.Vector2 = pygame.Vector2(0, 1)
        rotated_vector: pygame.Vector2 = unit_vector.rotate(self.rotation)
        speed_multiplier = SPEED_BOOST_MULTIPLIER if self.speed_boost_active else 1.0
        max_speed = PLAYER_MAX_SPEED * speed_multiplier
        acceleration: pygame.Vector2 = (
            rotated_vector * PLAYER_ACCELERATION * speed_multiplier * dt
        )
        self.velocity += acceleration
        # Cap velocity to max speed
        if self.velocity.length() > max_speed:
            self.velocity = self.velocity.normalize() * max_speed
        self.velocity *= PLAYER_FRICTION
        self.position += self.velocity * dt
        # Wrap around screen
        if self.position.x < 0:
            self.position.x = SCREEN_WIDTH
        elif self.position.x > SCREEN_WIDTH:
            self.position.x = 0
        if self.position.y < 0:
            self.position.y = SCREEN_HEIGHT
        elif self.position.y > SCREEN_HEIGHT:
            self.position.y = 0

    def shoot(self):
        cooldown = PLAYER_SHOOT_COOLDOWN_SECONDS
        if self.weapon_type == "rapid_fire":
            cooldown = PLAYER_SHOOT_COOLDOWN_SECONDS * 0.3

        if self.shoot_timer > 0:
            return

        self.shoot_timer = cooldown

        if self.weapon_type == "triple_shot":
            # Shoot three shots in a spread
            for angle_offset in [-15, 0, 15]:
                shot = Shot(self.position.x, self.position.y)
                shot.velocity = (
                    pygame.Vector2(0, 1).rotate(self.rotation + angle_offset)
                    * PLAYER_SHOOT_SPEED
                )
        else:
            shot = Shot(self.position.x, self.position.y)
            shot.velocity = (
                pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
            )

    def drop_bomb(self) -> Optional[Bomb]:
        if self.bomb_timer > 0:
            return None
        self.bomb_timer = BOMB_COOLDOWN
        bomb = Bomb(self.position.x, self.position.y)
        return bomb

    def collides_with_triangle(self, other) -> bool:
        """Check collision using triangular hitbox"""
        triangle_points = self.triangle()
        # Check if any point of triangle is within other's radius
        for point in triangle_points:
            if point.distance_to(other.position) <= other.radius:
                return True
        # Check if other's center is within triangle (simplified - check distance to triangle center)
        if self.position.distance_to(other.position) <= self.radius + other.radius:
            return True
        return False

    def update(self, dt: float) -> None:
        self.shoot_timer -= dt
        self.bomb_timer -= dt
        keys: tuple[int, ...] = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_SPACE]:
            self.shoot()
