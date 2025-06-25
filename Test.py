import pygame
import random

# Initialize pygame
pygame.init()
screen_width, screen_height = 1920, 1080
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
running = True

# Load and scale background
background_image = pygame.image.load('Space_S.webp')
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
background_rect = background_image.get_rect()

# Load and scale asteroid and explosion images
astroid_img = pygame.image.load('Astriod-removebg-preview.png')
explosion_img = pygame.image.load('cartoon-type-explosion-drawing-red-orange-yellow-violent-110908926-removebg-preview.png')
explosion_img = pygame.transform.scale(explosion_img, (100, 100))

# Font setup
font = pygame.font.SysFont("Arial", 36)

# Player setup
player = pygame.Vector2(screen_width, screen_height) / 2
angle = 180
speed = pygame.Vector2()

# Laser setup
lasers = []
laser_speed = 15

# Score and hit tracking
score = 0
hits = 0
max_hits = 3
exploded = False

# Asteroid sizes
ASTEROID_SIZES = {
    "large": 60,
    "medium": 40,
    "small": 20
}

# Create an asteroid
def create_asteroid(size="large", pos=None):
    if not pos:
        pos = pygame.Vector2(random.randint(0, screen_width), random.randint(0, screen_height))
    vel = pygame.Vector2(random.uniform(-2, 2), random.uniform(-2, 2))
    return {"pos": pos, "vel": vel, "size": size}

# Initial asteroid list
asteroids = [create_asteroid() for _ in range(10)]

# Function to wrap around screen edges
def wrap_position(pos):
    if pos.x < 0:
        pos.x = screen_width
    elif pos.x > screen_width:
        pos.x = 0
    if pos.y < 0:
        pos.y = screen_height
    elif pos.y > screen_height:
        pos.y = 0
    return pos

while running:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quit()
            if event.key == pygame.K_SPACE and not exploded:
                direction = pygame.Vector2(1, 0).rotate(angle)
                lasers.append({
                    "pos": player.copy(),
                    "dir": direction
                })

    if not exploded:
        # Player movement
        angle += keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
        speed.x += keys[pygame.K_UP] - keys[pygame.K_DOWN]
        speed *= 0.75
        player += speed.rotate(angle)
        player = wrap_position(player)

        # Asteroid movement
        for asteroid in asteroids:
            asteroid["pos"] += asteroid["vel"]
            asteroid["pos"] = wrap_position(asteroid["pos"])

        # Laser movement and border removal
        for laser in lasers[:]:
            laser["pos"] += laser["dir"] * laser_speed
            if (laser["pos"].x < 0 or laser["pos"].x > screen_width or
                laser["pos"].y < 0 or laser["pos"].y > screen_height):
                lasers.remove(laser)

        # Laser-asteroid collisions
        for laser in lasers[:]:
            laser_rect = pygame.Rect(laser["pos"].x, laser["pos"].y, 4, 4)
            for asteroid in asteroids[:]:
                size_px = ASTEROID_SIZES[asteroid["size"]]
                asteroid_rect = pygame.Rect(asteroid["pos"].x, asteroid["pos"].y, size_px, size_px)
                if laser_rect.colliderect(asteroid_rect):
                    lasers.remove(laser)
                    asteroids.remove(asteroid)
                    score += 10

                    # Split into smaller asteroids if possible
                    new_size = None
                    if asteroid["size"] == "large":
                        new_size = "medium"
                    elif asteroid["size"] == "medium":
                        new_size = "small"

                    if new_size:
                        for _ in range(2):
                            new_asteroid = create_asteroid(size=new_size, pos=asteroid["pos"].copy())
                            asteroids.append(new_asteroid)

                    # Always spawn one new large asteroid
                    asteroids.append(create_asteroid())

                    break

        # Player-asteroid collisions
        player_rect = pygame.Rect(player.x - 20, player.y - 20, 40, 40)
        for asteroid in asteroids:
            size_px = ASTEROID_SIZES[asteroid["size"]]
            asteroid_rect = pygame.Rect(asteroid["pos"].x, asteroid["pos"].y, size_px, size_px)
            if player_rect.colliderect(asteroid_rect):
                hits += 1
                asteroids.remove(asteroid)
                asteroids.append(create_asteroid())
                if hits >= max_hits:
                    exploded = True
                break

    # Draw everything
    screen.blit(background_image, background_rect)

    if not exploded:
        pygame.draw.circle(screen, "white", player, 20)
        pygame.draw.line(screen, "red", player, player + pygame.Vector2(21, 0).rotate(angle))
        for laser in lasers:
            pygame.draw.line(screen, "purple", laser["pos"], laser["pos"] + laser["dir"] * 15, 3)
    else:
        screen.blit(explosion_img, (player.x - 50, player.y - 50))

    # Draw asteroids
    for asteroid in asteroids:
        size_px = ASTEROID_SIZES[asteroid["size"]]
        scaled_img = pygame.transform.scale(astroid_img, (size_px, size_px))
        screen.blit(scaled_img, asteroid["pos"])

    # Draw hits (top-left) and score (top-right)
    hits_text = font.render(f"Hits: {hits}/{max_hits}", True, (255, 0, 0))
    screen.blit(hits_text, (20, 20))

    score_text = font.render(f"Score: {score}", True, (255, 255, 0))
    screen.blit(score_text, (screen_width - score_text.get_width() - 20, 20))

    pygame.display.flip()
    clock.tick(60)

    # End after explosion
    if exploded:
        pygame.time.delay(2000)
        running = False

pygame.quit()
