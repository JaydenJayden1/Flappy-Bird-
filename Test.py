import pygame
import random
import math

# Initialize pygame
pygame.init()
screen_width, screen_height = 1920, 1080
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
running = True
paused = False
game_started = False
game_over = False
you_win = False
level = 1  # Track current level
max_level = 2  # Define max levels

# Load and scale background
background_image = pygame.image.load('Space_S.webp')
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
background_rect = background_image.get_rect()

# Load images
astroid_img = pygame.image.load('Astriod-removebg-preview.png')
explosion_img = pygame.image.load('cartoon-type-explosion-drawing-red-orange-yellow-violent-110908926-removebg-preview.png')
explosion_img = pygame.transform.scale(explosion_img, (100, 100))
win_image = pygame.image.load('OIP__11_-removebg-preview.png')
win_image = pygame.transform.scale(win_image, (300, 300))

# New second-level win image
win_image_lvl2 = pygame.image.load('ast-uranus-removebg-preview.png')
win_image_lvl2 = pygame.transform.scale(win_image_lvl2, (300, 300))

ufo_img = pygame.image.load('ufo-cartoon-alien-spaceship-cosmic-ship-form-saucer-ufo-cartoon-alien-spaceship-cosmic-ship-form-saucer-181588751-removebg-preview.png')
ufo_img = pygame.transform.scale(ufo_img, (80, 60))  # Resize as needed

# Load sounds
explosion_sound = pygame.mixer.Sound('mixkit-explosion-hit-1704.wav')
laser_sound = pygame.mixer.Sound('mixkit-short-laser-gun-shot-1670.wav')
pygame.mixer.music.load('Not Like Us.mp3')

# Font setup
font = pygame.font.SysFont("Arial", 36)
big_font = pygame.font.SysFont("Arial", 100)

# Game timer
total_time = 5
start_ticks = None

# Invincibility
invincible = False
invincible_start = 0
invincible_duration = 10
invincible_uses = 5

# Asteroid sizes
ASTEROID_SIZES = {
    "large": 60,
    "medium": 40,
    "small": 20
}

# UFO variables
ufos = []
ufo_lasers = []
ufo_laser_speed = 5
ufo_shoot_interval = 10000
last_ufo_shot_time = 0
ufo_speed = 1.0

def reset_game(new_level=1):
    global player, angle, speed, lasers, score, hits, exploded, asteroids, start_ticks
    global paused, game_over, you_win, invincible, invincible_start, invincible_uses
    global ufos, ufo_lasers, last_ufo_shot_time, level, ufo_speed, total_time
    level = new_level
    player = pygame.Vector2(screen_width, screen_height) / 2
    angle = 180
    speed = pygame.Vector2()
    lasers = []
    score = 0
    hits = 0
    exploded = False
    game_over = False
    you_win = False
    paused = False
    invincible = False
    invincible_start = 0
    invincible_uses = 5 if level == 1 else 3
    start_ticks = pygame.time.get_ticks()
    asteroids.clear()
    ufos.clear()
    ufo_lasers.clear()
    last_ufo_shot_time = pygame.time.get_ticks()
    asteroid_count = 10 + 5 * (level - 1)  # More asteroids on level 2
    ufo_speed = 1.0 + 0.5 * (level - 1)  # UFOs get faster on level 2

    total_time = 5  # Timer now 5 seconds

    for _ in range(asteroid_count):
        asteroids.append(create_asteroid())
    ufos.append(create_ufo())
    pygame.mixer.music.play(-1)

def create_asteroid(size="large", pos=None):
    min_distance = 150
    while True:
        if not pos:
            pos = pygame.Vector2(random.randint(0, screen_width), random.randint(0, screen_height))
        if player.distance_to(pos) >= min_distance:
            break
        pos = None
    vel = pygame.Vector2(random.uniform(-2, 2), random.uniform(-2, 2))
    return {"pos": pos, "vel": vel, "size": size}

def create_ufo():
    min_distance = 200
    while True:
        pos = pygame.Vector2(random.randint(0, screen_width), random.randint(0, screen_height))
        if player.distance_to(pos) >= min_distance:
            break
    vel = pygame.Vector2(random.uniform(-ufo_speed, ufo_speed), random.uniform(-ufo_speed, ufo_speed))
    return {"pos": pos, "vel": vel}

def wrap_position(pos):
    if pos.x < 0: pos.x = screen_width
    elif pos.x > screen_width: pos.x = 0
    if pos.y < 0: pos.y = screen_height
    elif pos.y > screen_height: pos.y = 0
    return pos

button_width, button_height = 300, 100
button_rect = pygame.Rect(screen_width//2 - button_width//2, screen_height//2 - button_height//2, button_width, button_height)
asteroids = []

# Initialize player and variables
player = pygame.Vector2(screen_width, screen_height) / 2
angle = 180
speed = pygame.Vector2()
lasers = []
score = 0
hits = 0
exploded = False

# MAIN LOOP
while running:
    keys = pygame.key.get_pressed()
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not game_started:
            if event.type == pygame.MOUSEBUTTONDOWN and button_rect.collidepoint(event.pos):
                game_started = True
                reset_game(level)

        elif game_over:
            if event.type == pygame.KEYDOWN:
                # R: Next level (restart with next level)
                if event.key == pygame.K_r:
                    next_level = level + 1 if level < max_level else 1
                    reset_game(next_level)
                # ESC: Quit game
                elif event.key == pygame.K_ESCAPE:
                    running = False
                # SHIFT + C: Continue/unpause game
                elif event.key == pygame.K_c and (pygame.key.get_mods() & pygame.KMOD_SHIFT):
                    paused = False
                    game_over = False  # Continue game after game over (if desired)
                    # You might want to reset things or just unpause here depending on design

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
                elif event.key == pygame.K_f and not invincible and invincible_uses > 0:
                    invincible = True
                    invincible_start = pygame.time.get_ticks()
                    invincible_uses -= 1
                # Shift + C to continue even during gameplay pause
                elif event.key == pygame.K_c and (pygame.key.get_mods() & pygame.KMOD_SHIFT):
                    paused = False

    if not game_started:
        screen.blit(background_image, background_rect)
        pygame.draw.rect(screen, (0, 255, 0), button_rect)
        play_text = big_font.render("PLAY", True, (0, 0, 0))
        screen.blit(play_text, (button_rect.centerx - play_text.get_width()//2, button_rect.centery - play_text.get_height()//2))
        info_text1 = font.render("Press P to pause during the game", True, (255, 255, 255))
        info_text2 = font.render("Press F for 10 seconds of invincibility (5 uses)", True, (255, 255, 255))
        screen.blit(info_text1, (screen_width // 2 - info_text1.get_width() // 2, button_rect.bottom + 30))
        screen.blit(info_text2, (screen_width // 2 - info_text2.get_width() // 2, button_rect.bottom + 70))
        pygame.display.flip()
        clock.tick(60)
        continue

    if game_over:
        screen.blit(background_image, background_rect)
        if you_win:
            win_text = big_font.render("YOU WIN", True, (255, 255, 0))
            screen.blit(win_text, (screen_width//2 - win_text.get_width()//2, screen_height//2 - 100))
            # Show correct win image depending on level
            if level == 1:
                screen.blit(win_image, (screen_width - win_image.get_width() - 100, screen_height//2 - win_image.get_height()//2))
            else:
                screen.blit(win_image_lvl2, (screen_width - win_image_lvl2.get_width() - 100, screen_height//2 - win_image_lvl2.get_height()//2))
        else:
            lose_text = big_font.render("YOU LOSE", True, (255, 0, 0))
            screen.blit(lose_text, (screen_width//2 - lose_text.get_width()//2, screen_height//2 - 100))
        tip_text = font.render("Press R to go to Next Level - Press ESC to Quit - Shift+C to Continue", True, (255, 255, 255))
        screen.blit(tip_text, (screen_width//2 - tip_text.get_width()//2, screen_height//2 + 100))
        pygame.display.flip()
        clock.tick(60)
        continue

    if paused:
        pause_text = font.render("PAUSED", True, (255, 255, 255))
        screen.blit(pause_text, (screen_width // 2 - pause_text.get_width() // 2, 100))
        tip_text = font.render("Press Shift+C to Continue or P to Pause", True, (255, 255, 255))
        screen.blit(tip_text, (screen_width // 2 - tip_text.get_width() // 2, 150))
        pygame.display.flip()
        clock.tick(60)
        continue

    # Handle invincibility timing
    if invincible:
        elapsed = (pygame.time.get_ticks() - invincible_start) / 1000
        if elapsed >= invincible_duration:
            invincible = False

    if not exploded:
        angle += keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
        speed.x += keys[pygame.K_UP] - keys[pygame.K_DOWN]
        speed *= 0.75
        player += speed.rotate(angle)
        player = wrap_position(player)

        for asteroid in asteroids:
            asteroid["pos"] += asteroid["vel"]
            asteroid["pos"] = wrap_position(asteroid["pos"])

        # UFO movement
        for ufo in ufos:
            ufo["pos"] += ufo["vel"]
            ufo["pos"] = wrap_position(ufo["pos"])

        # UFO shooting every 10 seconds
        if current_time - last_ufo_shot_time > ufo_shoot_interval:
            last_ufo_shot_time = current_time
            for ufo in ufos:
                direction = (player - ufo["pos"]).normalize()
                ufo_lasers.append({"pos": ufo["pos"].copy(), "dir": direction})

        # Laser movement and removal
        for laser in lasers[:]:
            laser["pos"] += laser["dir"] * 15
            if not (0 <= laser["pos"].x <= screen_width and 0 <= laser["pos"].y <= screen_height):
                lasers.remove(laser)

        for ufo_laser in ufo_lasers[:]:
            ufo_laser["pos"] += ufo_laser["dir"] * ufo_laser_speed
            if not (0 <= ufo_laser["pos"].x <= screen_width and 0 <= ufo_laser["pos"].y <= screen_height):
                ufo_lasers.remove(ufo_laser)

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
                    if asteroid["size"] == "large":
                        for _ in range(2):
                            asteroids.append(create_asteroid("medium", pos=asteroid["pos"].copy()))
                    elif asteroid["size"] == "medium":
                        for _ in range(2):
                            asteroids.append(create_asteroid("small", pos=asteroid["pos"].copy()))
                    asteroids.append(create_asteroid())
                    break

        # Player collision with asteroids
        player_rect = pygame.Rect(player.x - 20, player.y - 20, 40, 40)
        for asteroid in asteroids:
            size_px = ASTEROID_SIZES[asteroid["size"]]
            asteroid_rect = pygame.Rect(asteroid["pos"].x, asteroid["pos"].y, size_px, size_px)
            if player_rect.colliderect(asteroid_rect):
                if not invincible:
                    hits += 1
                    asteroids.remove(asteroid)
                    asteroids.append(create_asteroid())
                    if hits >= 3:
                        explosion_sound.play()
                        pygame.mixer.music.stop()
                        exploded = True
                break

        # Player collision with UFO lasers
        for ufo_laser in ufo_lasers[:]:
            laser_rect = pygame.Rect(ufo_laser["pos"].x, ufo_laser["pos"].y, 6, 6)
            if player_rect.colliderect(laser_rect):
                if not invincible:
                    hits += 1
                    ufo_lasers.remove(ufo_laser)
                    if hits >= 3:
                        explosion_sound.play()
                        pygame.mixer.music.stop()
                        exploded = True
                else:
                    ufo_lasers.remove(ufo_laser)

    # Draw everything
    screen.blit(background_image, background_rect)

    if not exploded:
        color = "blue" if invincible else "white"
        pygame.draw.circle(screen, color, player, 20)
        pygame.draw.line(screen, "red", player, player + pygame.Vector2(21, 0).rotate(angle))
        for laser in lasers:
            pygame.draw.line(screen, "purple", laser["pos"], laser["pos"] + laser["dir"] * 15, 3)
    else:
        screen.blit(explosion_img, (player.x - 50, player.y - 50))

    for asteroid in asteroids:
        size_px = ASTEROID_SIZES[asteroid["size"]]
        scaled_img = pygame.transform.scale(astroid_img, (size_px, size_px))
        screen.blit(scaled_img, asteroid["pos"])

    # Draw UFOs
    for ufo in ufos:
        screen.blit(ufo_img, ufo["pos"])

    # Draw UFO lasers
    for ufo_laser in ufo_lasers:
        pygame.draw.circle(screen, (0, 255, 0), (int(ufo_laser["pos"].x), int(ufo_laser["pos"].y)), 6)

    hits_text = font.render(f"Hits: {hits}/3", True, (255, 0, 0))
    screen.blit(hits_text, (20, 20))

    score_text = font.render(f"Score: {score}", True, (255, 255, 0))
    screen.blit(score_text, (screen_width - score_text.get_width() - 20, 20))

    if invincible:
        remaining = max(0, invincible_duration - int((pygame.time.get_ticks() - invincible_start) / 1000))
        inv_text = font.render(f"Invincible: {remaining}s", True, (0, 255, 255))
        screen.blit(inv_text, (screen_width - inv_text.get_width() - 20, screen_height - 50))

    seconds_passed = (pygame.time.get_ticks() - start_ticks) / 1000 if start_ticks else 0
    remaining_time = max(0, total_time - int(seconds_passed))
    minutes = remaining_time // 60
    seconds = remaining_time % 60
    timer_text = font.render(f"Time: {int(minutes):02d}:{int(seconds):02d}", True, (255, 255, 255))
    screen.blit(timer_text, (screen_width // 2 - timer_text.get_width() // 2, screen_height - 50))

    pygame.display.flip()
    clock.tick(60)

    # When game ends and not already in game_over state
    if (exploded or remaining_time <= 0) and not game_over:
        pygame.mixer.music.stop()
        pygame.time.delay(1000)
        game_over = True
        if not exploded:
            you_win = True
            # If won level 1, automatically go to level 2 after 2 seconds delay
            # You can remove this if you want manual control with R
            # pygame.time.delay(2000)
            # reset_game(new_level=2)

pygame.quit()
