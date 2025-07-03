import pygame
pygame.init()

pygame.display.set_caption('Моя игра')

icon = pygame.image.load('icon.png')

pygame.display.set_icon(icon)

# Размеры экранаё
screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h

# Создание экрана
screen = pygame.display.set_mode((screen_width, screen_height))

# Загрузка изображения персонажа
player_img = pygame.image.load('assets/images/player/playerR_1.png')

# Изменение размеров изображения в зависимости от размера экрана
player_width = screen_width // 10  # Размер персонажа будет 1/10 от ширины экрана
player_height = screen_height // 5  # Размер персонажа будет 1/10 от высоты экрана
player_img = pygame.transform.scale(player_img, (player_width, player_height))

player_x = 370
player_y = screen_height - (player_height + 80)

player_speed = 15.5
jump_speed = 20
gravity = 1

playerR_frame = [
        pygame.transform.scale(pygame.image.load('assets/images/player/playerR_1.png'), (player_width, player_height)),
        pygame.transform.scale(pygame.image.load('assets/images/player/playerR_2.png'), (player_width, player_height)),
        pygame.transform.scale(pygame.image.load('assets/images/player/playerR_3.png'), (player_width, player_height)),
        pygame.transform.scale(pygame.image.load('assets/images/player/playerR_4.png'), (player_width, player_height)),
        pygame.transform.scale(pygame.image.load('assets/images/player/playerR_5.png'), (player_width, player_height))
                ]
playerL_frame = [
        pygame.transform.scale(pygame.image.load('assets/images/player/playerL_1.png'), (player_width, player_height)),
        pygame.transform.scale(pygame.image.load('assets/images/player/playerL_2.png'), (player_width, player_height)),
        pygame.transform.scale(pygame.image.load('assets/images/player/playerL_3.png'), (player_width, player_height)),
        pygame.transform.scale(pygame.image.load('assets/images/player/playerL_4.png'), (player_width, player_height)),
        pygame.transform.scale(pygame.image.load('assets/images/player/playerL_5.png'), (player_width, player_height))
                ]

playerJR_frame = [
        pygame.transform.scale(pygame.image.load('assets/images/player/playerJR.png'), (player_width, player_height)),
        pygame.transform.scale(pygame.image.load('assets/images/player/playerR_1.png'), (player_width, player_height))
]
playerJL_frame = [
        pygame.transform.scale(pygame.image.load('assets/images/player/playerJL.png'), (player_width, player_height)),
        pygame.transform.scale(pygame.image.load('assets/images/player/playerL_1.png'), (player_width, player_height))
]

background_img = pygame.image.load('assets/images/background.png')
background_img = pygame.transform.scale(background_img, (screen_width, screen_height))
# звук бега и прыжка
run_sound = pygame.mixer.Sound("assets/sounds/running.mp3")
jump_sound = pygame.mixer.Sound("assets/sounds/jumping.mp3")
jump_sound.set_volume(0.4)
# фоновая музыка
pygame.mixer.music.load("assets/sounds/background_music.mp3")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)

current_frame = 0
frame_rate = 10
last_update_time = pygame.time.get_ticks()
last_direction = 'right'

is_jumping = False
jump_velocity = 0

def draw_player(x, y, frames, moving, jumping = False):
    global current_frame, last_update_time
    if jumping:
        screen.blit(frames[0], (x, y))
    elif moving:
        current_time = pygame.time.get_ticks()
        if current_time - last_update_time > 1000 // frame_rate:
            current_frame = (current_frame + 1) % len(frames)
            last_update_time = current_time
        screen.blit(frames[current_frame], (x, y))
    else:
        screen.blit(frames[0], (x, y))

# Игровой цикл
running = True
running_sound_playing = False
clock = pygame.time.Clock()
while running:
    # Задний фон
    screen.blit(background_img, (0, 0))

    keys = pygame.key.get_pressed()
    if is_jumping:
         if running_sound_playing:
             run_sound.stop()
             running_sound_playing = False
    else:
         if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
             if not  running_sound_playing:
                 run_sound.play(-1)
                 running_sound_playing = True
         else:
             if  running_sound_playing:
                 run_sound.stop()
                 running_sound_playing = False


    # В игровом цикле, чтобы двигать персонажа

    if keys[pygame.K_LEFT]:
        player_x -= player_speed
        if is_jumping:
            draw_player(player_x, player_y, playerJL_frame, True, True)
        else:  
            draw_player(player_x, player_y, playerL_frame, True)
        last_direction  = "left"



    elif keys[pygame.K_RIGHT]:
        player_x += player_speed
        if is_jumping:
            draw_player(player_x, player_y, playerJR_frame, True, True)
        else:
            draw_player(player_x, player_y, playerR_frame, True)
        last_direction  = "right"
    else:
        if is_jumping:
            if last_direction == "left":
                draw_player(player_x, player_y, playerJL_frame, False, True)
            else:
                draw_player(player_x, player_y, playerJR_frame, False, True)
        else:
            if last_direction == "left":
                draw_player(player_x, player_y, playerL_frame, False)
            else:
                draw_player(player_x, player_y, playerR_frame, False)


    if not is_jumping:
        if keys[pygame.K_UP]:
            is_jumping = True
            jump_velocity = -jump_speed
            jump_sound.play()



    if is_jumping:
        player_y += jump_velocity
        jump_velocity += gravity
        if player_y > screen_height - (player_height + 80):
            player_y = screen_height - (player_height + 80)
            is_jumping = False
            jump_sound.play()




    if player_x < -player_width:
        player_x = -player_width

        # обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False


    pygame.display.update()
    # В начале игрового цикла
    clock.tick(60)

pygame.quit()