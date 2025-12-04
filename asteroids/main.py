import pygame
import random

from asteroids.asteroid import Asteroid
from asteroids.asteroidfield import AsteroidField
from asteroids.bomb import Bomb
from asteroids.constants import (
    BOMB_RADIUS,
    POINTS_PER_ASTEROID,
    POWERUP_SPAWN_RATE_SECONDS,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)
from asteroids.explosion import Explosion, ExplosionParticle
from asteroids.logger import log_event, log_state
from asteroids.player import Player
from asteroids.powerup import PowerUp, PowerUpManager
from asteroids.shot import Shot


_starfield_cache = None


def draw_background(screen: pygame.Surface) -> None:
    """Draw a starfield background"""
    global _starfield_cache
    if _starfield_cache is None:
        # Generate starfield once
        _starfield_cache = []
        for _ in range(100):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            brightness = random.randint(100, 255)
            _starfield_cache.append((x, y, brightness))

    screen.fill((10, 10, 20))  # Dark blue-black background
    # Draw stars
    for x, y, brightness in _starfield_cache:
        pygame.draw.circle(screen, (brightness, brightness, brightness), (x, y), 1)


def show_game_over_screen(screen: pygame.Surface, score: int) -> bool:
    """Show game over screen, return True if player wants to restart"""
    font_large = pygame.font.Font(None, 72)
    font_medium = pygame.font.Font(None, 48)
    font_small = pygame.font.Font(None, 36)

    game_over_text = font_large.render("GAME OVER", True, (255, 0, 0))
    score_text = font_medium.render(f"Final Score: {score}", True, (255, 255, 255))
    restart_text = font_small.render(
        "Press R to Restart or Q to Quit", True, (200, 200, 200)
    )

    game_over_rect = game_over_text.get_rect(
        center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 100)
    )
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
    restart_rect = restart_text.get_rect(
        center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 100)
    )

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                if event.key == pygame.K_q:
                    return False

        screen.fill((0, 0, 0))
        screen.blit(game_over_text, game_over_rect)
        screen.blit(score_text, score_rect)
        screen.blit(restart_text, restart_rect)
        pygame.display.flip()


def init_game():
    """Initialize game objects and return them"""
    updatable: pygame.sprite.Group = pygame.sprite.Group()
    drawable: pygame.sprite.Group = pygame.sprite.Group()
    asteroids: pygame.sprite.Group = pygame.sprite.Group()
    shots: pygame.sprite.Group = pygame.sprite.Group()
    powerups: pygame.sprite.Group = pygame.sprite.Group()
    bombs: pygame.sprite.Group = pygame.sprite.Group()
    explosions: pygame.sprite.Group = pygame.sprite.Group()

    Asteroid.containers = (asteroids, updatable, drawable)  # type: ignore
    Shot.containers = (shots, updatable, drawable)  # type: ignore
    Bomb.containers = (bombs, updatable, drawable)  # type: ignore
    PowerUp.containers = (powerups, updatable, drawable)  # type: ignore
    ExplosionParticle.containers = (explosions, updatable, drawable)  # type: ignore

    AsteroidField.containers = updatable  # type: ignore
    AsteroidField()  # type: ignore

    Player.containers = (updatable, drawable)  # type: ignore
    player: Player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    return {
        "updatable": updatable,
        "drawable": drawable,
        "asteroids": asteroids,
        "shots": shots,
        "powerups": powerups,
        "bombs": bombs,
        "explosions": explosions,
        "player": player,
    }


def main() -> None:
    pygame.init()
    screen: pygame.Surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock: pygame.time.Clock = pygame.time.Clock()
    pygame.display.set_caption("Asteroids")

    # Reset starfield on new game
    global _starfield_cache
    _starfield_cache = None

    while True:
        game_objects = init_game()
        updatable = game_objects["updatable"]
        drawable = game_objects["drawable"]
        asteroids = game_objects["asteroids"]
        shots = game_objects["shots"]
        powerups = game_objects["powerups"]
        bombs = game_objects["bombs"]
        explosions = game_objects["explosions"]
        player = game_objects["player"]

        powerup_manager = PowerUpManager()
        score = 0
        powerup_spawn_timer = 0.0
        game_over = False
        paused = False
        font = pygame.font.Font(None, 48)
        pause_font = pygame.font.Font(None, 72)

        dt: float = 0
        while not game_over:
            log_state()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        paused = not paused

            if not paused:
                # Update power-up manager
                powerup_manager.update(dt)
                player.shield_active = powerup_manager.shield_active
                player.speed_boost_active = powerup_manager.speed_boost_active
                player.rapid_fire_active = powerup_manager.rapid_fire_active
                player.triple_shot_active = powerup_manager.triple_shot_active

                # Handle bomb dropping
                keys = pygame.key.get_pressed()
                if keys[pygame.K_b]:
                    bomb_result = player.drop_bomb()
                    if bomb_result:
                        bomb_result.containers = (bombs, updatable, drawable)  # type: ignore
                        bomb_result.add((bombs, updatable, drawable))  # type: ignore

                updatable.update(dt)

                # Spawn power-ups (only when not paused)
                powerup_spawn_timer += dt
                if powerup_spawn_timer > POWERUP_SPAWN_RATE_SECONDS and len(powerups) == 0:
                    powerup_spawn_timer = 0
                    x = random.randint(50, SCREEN_WIDTH - 50)
                    y = random.randint(50, SCREEN_HEIGHT - 50)
                    powerup = PowerUp(x, y)
                    powerup.containers = (powerups, updatable, drawable)  # type: ignore
                    powerup.add((powerups, updatable, drawable))  # type: ignore

            # Check collisions: player vs asteroids
            for asteroid in asteroids:
                if player.shield_active:
                    # Shield protects from one hit
                    if asteroid.collides_with(player):
                        log_event("player_hit_shield")
                        asteroid.split()
                        score += POINTS_PER_ASTEROID
                        Explosion.create(
                            asteroid.position.x,
                            asteroid.position.y,
                            (explosions, updatable, drawable),
                        )
                        powerup_manager.shield_active = False
                        player.shield_active = False
                else:
                    # Use triangular hitbox
                    if player.collides_with_triangle(asteroid):
                        log_event("player_hit")
                        game_over = True
                        break

            # Check collisions: shots vs asteroids
            for asteroid in list(asteroids):
                for shot in list(shots):
                    if shot.collides_with(asteroid):
                        log_event("asteroid_shot")
                        shot.kill()
                        asteroid.split()
                        score += POINTS_PER_ASTEROID
                        Explosion.create(
                            asteroid.position.x,
                            asteroid.position.y,
                            (explosions, updatable, drawable),
                        )
                        break

            # Check collisions: bombs vs asteroids
            for bomb in list(bombs):
                if bomb.exploded:
                    # Bomb exploded, destroy nearby asteroids
                    for asteroid in list(asteroids):
                        if bomb.position.distance_to(asteroid.position) <= BOMB_RADIUS:
                            log_event("asteroid_destroyed_by_bomb")
                            asteroid.split()
                            score += POINTS_PER_ASTEROID
                            Explosion.create(
                                asteroid.position.x,
                                asteroid.position.y,
                                (explosions, updatable, drawable),
                            )
                    Explosion.create(
                        bomb.position.x,
                        bomb.position.y,
                        (explosions, updatable, drawable),
                    )
                    bomb.kill()

            # Check collisions: player vs power-ups
            for powerup in list(powerups):
                if powerup.collides_with(player):
                    log_event("powerup_collected", type=powerup.powerup_type)
                    powerup_manager.activate(powerup.powerup_type)
                    powerup.kill()

            # Draw everything
            draw_background(screen)

            for obj in drawable:
                obj.draw(screen)

            # Draw score (top left, always on top)
            score_text = font.render(f"Score: {score}", True, (255, 255, 255))
            screen.blit(score_text, (10, 10))

            # Draw pause screen
            if paused:
                pause_text = pause_font.render("PAUSED", True, (255, 255, 255))
                pause_rect = pause_text.get_rect(
                    center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                )
                # Draw semi-transparent overlay
                overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                overlay.set_alpha(128)
                overlay.fill((0, 0, 0))
                screen.blit(overlay, (0, 0))
                screen.blit(pause_text, pause_rect)

            # Draw power-up status
            y_offset = 60
            if powerup_manager.shield_active:
                shield_text = font.render(
                    f"Shield: {powerup_manager.shield_timer:.1f}s", True, (0, 150, 255)
                )
                screen.blit(shield_text, (10, y_offset))
                y_offset += 40
            if powerup_manager.speed_boost_active:
                speed_text = font.render(
                    f"Speed Boost: {powerup_manager.speed_boost_timer:.1f}s",
                    True,
                    (255, 200, 0),
                )
                screen.blit(speed_text, (10, y_offset))
                y_offset += 40
            if powerup_manager.rapid_fire_active:
                rapid_text = font.render(
                    f"Rapid Fire: {powerup_manager.rapid_fire_timer:.1f}s",
                    True,
                    (255, 0, 0),
                )
                screen.blit(rapid_text, (10, y_offset))
                y_offset += 40
            if powerup_manager.triple_shot_active:
                triple_text = font.render(
                    f"Triple Shot: {powerup_manager.triple_shot_timer:.1f}s",
                    True,
                    (0, 255, 0),
                )
                screen.blit(triple_text, (10, y_offset))

            pygame.display.flip()

            # limits game to 60 fps
            dt = clock.tick(60) / 1000

        # Game over - show screen and check for restart
        if not show_game_over_screen(screen, score):
            return

