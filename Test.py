import pygame
import random

# Initialize pygame
pygame.init()
screen_width, screen_height = 1920, 1080
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
running = True
paused = False
game_started = False
game_over = False

# Load and scale background
background_image = pygame.image.load('Space_S.webp')
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
background_rect = background_image.get_rect()

# Load and scale asteroid and explosion images
astroid_img = pygame.image.load('Astriod-removebg-preview.png')
explosion_img = pygame.image.load('cartoon-type-explosion-drawing-red-orange-yellow-violent-110908926-removebg-preview.png')
explosion_img = pygame.transform.scale(explosion_img, (100, 100))

# Load sounds
explosion_sound = pygame.mixer.Sound('mixkit-explosion-hit-1704.wav')
laser_sound = pygame.mixer.Sound('mixkit-short-laser-gun-shot-1670.wav')

# Load background music
pygame.mixer.music.load('Not Like Us.mp3')

# Font setup
font = pygame.font.SysFont("Arial", 36)
big_font = pygame.font.SysFont("Arial", 100)

# Game variables
total_time = 300  # seconds
start_ticks = None

# Setup function to reset game state
def reset_game():
    global player, angle, speed, lasers, score, hits, exploded, asteroids, start_ticks, paused, game_over
    player = pygame.Vector2(screen_width, screen_height) / 2
    angle = 180
    speed = pygame.Vector2()
    lasers = []
    score = 0
    hits = 0
    exploded = False
    asteroids = [create_asteroid() for _ in range(10)]
    start_ticks = pygame.time.get_ticks()
    paused = False
    game_over = False
    pygame.mixer.music.play(-1)  # 🔁 Play background music loop

# Asteroid sizes
ASTEROID_SIZES = {
    "large": 60,
    "medium": 40,
    "small": 20
}

def create_asteroid(size="large", pos=None):
    min_distance = 150  # Minimum distance from player
    while True:
        if not pos:
            pos = pygame.Vector2(random.randint(0, screen_width), random.randint(0, screen_height))
        if player.distance_to(pos) >= min_distance:
            break
        pos = None  # Force re-roll if too close
    vel = pygame.Vector2(random.uniform(-2, 2), random.uniform(-2, 2))
    return {"pos": pos, "vel": vel, "size": size}

asteroids = []

# Function to wrap around screen edges
def wrap_position(pos):
    if pos.x < 0: pos.x = screen_width
    elif pos.x > screen_width: pos.x = 0
    if pos.y < 0: pos.y = screen_height
    elif pos.y > screen_height: pos.y = 0
    return pos

# Button setup
button_width, button_height = 300, 100
button_rect = pygame.Rect(screen_width//2 - button_width//2, screen_height//2 - button_height//2, button_width, button_height)

while running:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not game_started:
            if event.type == pygame.MOUSEBUTTONDOWN and button_rect.collidepoint(event.pos):
                game_started = True
                reset_game()

        elif game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()
                elif event.key == pygame.K_ESCAPE:
                    running = False

        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_p:
                    paused = not paused
                elif event.key == pygame.K_SPACE and not exploded and not paused:
                    direction = pygame.Vector2(1, 0).rotate(angle)
                    lasers.append({"pos": player.copy(), "dir": direction})
                    laser_sound.play()

    # Start screen
    if not game_started:
        screen.fill((0, 0, 0))
        screen.blit(background_image, background_rect)
        pygame.draw.rect(screen, (0, 255, 0), button_rect)
        play_text = big_font.render("PLAY", True, (0, 0, 0))
        screen.blit(play_text, (button_rect.centerx - play_text.get_width()//2, button_rect.centery - play_text.get_height()//2))
        info_text = font.render("Press P to pause during the game", True, (255, 255, 255))
        screen.blit(info_text, (screen_width // 2 - info_text.get_width() // 2, button_rect.bottom + 30))
        pygame.display.flip()
        clock.tick(60)
        continue

    # Game over screen
    if game_over:
        screen.blit(background_image, background_rect)
        lose_text = big_font.render("YOU LOSE", True, (255, 0, 0))
        screen.blit(lose_text, (screen_width//2 - lose_text.get_width()//2, screen_height//2 - 100))
        tip_text = font.render("Press R to Restart - Press ESC to Quit", True, (255, 255, 255))
        screen.blit(tip_text, (screen_width//2 - tip_text.get_width()//2, screen_height//2 + 50))
        pygame.display.flip()
        clock.tick(60)
        continue

    if paused:
        pause_text = font.render("PAUSED", True, (255, 255, 255))
        screen.blit(pause_text, (screen_width // 2 - pause_text.get_width() // 2, 100))
        pygame.display.flip()
        clock.tick(60)
        continue

    if not exploded:
        angle += keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
        speed.x += keys[pygame.K_UP] - keys[pygame.K_DOWN]
        speed *= 0.75
        player += speed.rotate(angle)
        player = wrap_position(player)

        for asteroid in asteroids:
            asteroid["pos"] += asteroid["vel"]
            asteroid["pos"] = wrap_position(asteroid["pos"])

        for laser in lasers[:]:
            laser["pos"] += laser["dir"] * 15
            if laser["pos"].x < 0 or laser["pos"].x > screen_width or laser["pos"].y < 0 or laser["pos"].y > screen_height:
                lasers.remove(laser)

        for laser in lasers[:]:
            laser_rect = pygame.Rect(laser["pos"].x, laser["pos"].y, 4, 4)
            for asteroid in asteroids[:]:
                size_px = ASTEROID_SIZES[asteroid["size"]]
                asteroid_rect = pygame.Rect(asteroid["pos"].x, asteroid["pos"].y, size_px, size_px)
                if laser_rect.colliderect(asteroid_rect):
                    lasers.remove(laser)
                    asteroids.remove(asteroid)
                    score += 10
                    new_size = "medium" if asteroid["size"] == "large" else "small" if asteroid["size"] == "medium" else None
                    if new_size:
                        for _ in range(2):
                            asteroids.append(create_asteroid(size=new_size, pos=asteroid["pos"].copy()))
                    asteroids.append(create_asteroid())
                    break

        player_rect = pygame.Rect(player.x - 20, player.y - 20, 40, 40)
        for asteroid in asteroids:
            size_px = ASTEROID_SIZES[asteroid["size"]]
            asteroid_rect = pygame.Rect(asteroid["pos"].x, asteroid["pos"].y, size_px, size_px)
            if player_rect.colliderect(asteroid_rect):
                hits += 1
                asteroids.remove(asteroid)
                asteroids.append(create_asteroid())
                if hits >= 3:
                    explosion_sound.play()
                    pygame.mixer.music.stop()  # ⛔ Stop background music on death
                    exploded = True
                break

    screen.blit(background_image, background_rect)

    if not exploded:
        pygame.draw.circle(screen, "white", player, 20)
        pygame.draw.line(screen, "red", player, player + pygame.Vector2(21, 0).rotate(angle))
        for laser in lasers:
            pygame.draw.line(screen, "purple", laser["pos"], laser["pos"] + laser["dir"] * 15, 3)
    else:
        screen.blit(explosion_img, (player.x - 50, player.y - 50))

    for asteroid in asteroids:
        size_px = ASTEROID_SIZES[asteroid["size"]]
        scaled_img = pygame.transform.scale(astroid_img, (size_px, size_px))
        screen.blit(scaled_img, asteroid["pos"])

    hits_text = font.render(f"Hits: {hits}/3", True, (255, 0, 0))
    screen.blit(hits_text, (20, 20))

    score_text = font.render(f"Score: {score}", True, (255, 255, 0))
    screen.blit(score_text, (screen_width - score_text.get_width() - 20, 20))

    seconds_passed = (pygame.time.get_ticks() - start_ticks) / 1000 if start_ticks else 0
    remaining_time = max(0, total_time - int(seconds_passed))
    minutes = remaining_time // 60
    seconds = remaining_time % 60
    timer_text = font.render(f"Time: {int(minutes):02d}:{int(seconds):02d}", True, (255, 255, 255))
    screen.blit(timer_text, (screen_width // 2 - timer_text.get_width() // 2, screen_height - 50))

    pygame.display.flip()
    clock.tick(60)

    if (exploded or remaining_time <= 0) and not game_over:
        pygame.mixer.music.stop()  # ⛔ Stop music if time runs out too
        pygame.time.delay(1000)
        game_over = True

pygame.quit()
