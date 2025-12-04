import sys
import pygame

from asteroid import Asteroid
from asteroidfield import AsteroidField
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from logger import log_state, log_event
from player import Player
from shot import Shot


def main() -> None:
    pygame.init()
    screen: pygame.Surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock: pygame.time.Clock = pygame.time.Clock()

    updatable: pygame.sprite.Group = pygame.sprite.Group()
    drawable: pygame.sprite.Group = pygame.sprite.Group()
    asteroids: pygame.sprite.Group = pygame.sprite.Group()
    shots: pygame.sprite.Group = pygame.sprite.Group()

    Asteroid.containers = (asteroids, updatable, drawable)  # type: ignore
    Shot.containers = (shots, updatable, drawable)  # type: ignore
    AsteroidField.containers = updatable  # type: ignore
    asteroid_field: AsteroidField = AsteroidField()  # type: ignore

    Player.containers = (updatable, drawable)  # type: ignore
    player: Player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    dt: float = 0
    while True:
        log_state()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        updatable.update(dt)
        for asteroid in asteroids:
            if asteroid.collides_with(player):
                log_event("player_hit")
                print("Game over!")
                sys.exit()

        screen.fill("black")

        for obj in drawable:
            obj.draw(screen)

        pygame.display.flip()

        # limits game to 60 fps
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
