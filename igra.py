import pygame  # Импортируем библиотеку pygame для работы с графикой и аудио
import random  # Импортируем библиотеку random для работы с генерации случайных чисел
import sys      # Импортируем библиотеку sys для коректного завершения exe файла
clock = pygame.time.Clock()  # Создаем объект Clock для управления временем
pygame.init()  # Инициализируем pygame
#===========================================Настройки окна игры========================================================
window_width = 1920 # Задаем ширину окна
window_height = 1080  # Задаем высоту окна
screen = pygame.display.set_mode((window_width, window_height))  # Создаем окно с заданным размером
pygame.display.set_caption('First Game')  # Устанавливаем заголовок окна
pygame.mouse.set_visible(False) # отключаем отображения курсора мыши
icon = pygame.image.load('img/icon.png').convert_alpha()  # Загружаем иконку окна
pygame.display.set_icon(icon)  # Устанавливаем иконку окна
#======================================================================================================================
#==========================================Загрузка звуков=============================================================
bg_sound = pygame.mixer.music.load('sound/bg.mp3')  # Загружаем фоновую музыку
bg_sound = pygame.mixer.music.play(-1)  # Воспроизводим фоновую музыку в цикле
jump_sound = pygame.mixer.Sound('sound/jump.mp3')#
arrow_sound = pygame.mixer.Sound('sound/arrow_push.mp3')#
arrow_balista_sound = pygame.mixer.Sound('sound/arrow_balista.mp3')#
enemy_hit = pygame.mixer.Sound('sound/hit.mp3')#
player_loss = pygame.mixer.Sound('sound/loss.mp3')#
arrow_sound_add = pygame.mixer.Sound('sound/add_arrow.mp3')#
add_coin = pygame.mixer.Sound('sound/coin.mp3')#
fireboll_sound = pygame.mixer.Sound('sound/fireboll.mp3')#
game_complite_sound = pygame.mixer.Sound('sound/game_complite.mp3')
#======================================================================================================================
#=======================================Загрузка шрифтов, картинок интерфейса и объявление текста======================
font_gameover = pygame.font.Font('font/PressStart2P-Regular.ttf', 80)
font_restart = pygame.font.Font('font/PressStart2P-Regular.ttf', 40)
font_arrow = pygame.font.Font('font/PressStart2P-Regular.ttf', 60)
font_coin = pygame.font.Font('font/PressStart2P-Regular.ttf', 60)
font_best_score = pygame.font.Font('font/PressStart2P-Regular.ttf', 60)
arrow_counter = pygame.image.load('img/arrow_сounter.png').convert_alpha()
coin_counter = pygame.image.load('img/coin.png').convert_alpha()
best_score_image = pygame.image.load('img/best_score.png').convert_alpha()
gameover_label = font_gameover.render('Game Over', False, 'grey')
restart_label = font_restart.render('Press R to restart game', False, (11, 218, 81))
#=============================================Блок заднего фона========================================================
# Загружаем фоновое изображение
background_image = pygame.image.load('img/background.png').convert_alpha()
background_endgame = pygame.image.load('img/background_complite.png').convert_alpha()
# Масштабируем фоновое изображение до размеров окна
background_image = pygame.transform.scale(background_image, (window_width, window_height))
background_endgame = pygame.transform.scale(background_endgame, (window_width, window_height))
# Начальные координаты заднего фона
background_x = 0
background_y = 0
# Скорость движения заднего фона
background_speed = 4
# Функция отрисовки заднего фона
def draw_background(x, y):
    screen.blit(background_image, (x, y))
    screen.blit(background_image, (x + window_width, y))
# #=====================================================================================================================
# #================================================Блок кода игрока=====================================================
# # Загружаем изображения для анимации движения влево
player_images_left = [
    pygame.image.load('img/player_left/player-left1.png').convert_alpha(),
    pygame.image.load('img/player_left/player-left2.png').convert_alpha(),
    pygame.image.load('img/player_left/player-left3.png').convert_alpha(),
    pygame.image.load('img/player_left/player-left4.png').convert_alpha(),
]
# Загружаем изображения для анимации движения вправо
player_images_right = [
    pygame.image.load('img/player_right/player-right1.png').convert_alpha(),
    pygame.image.load('img/player_right/player-right2.png').convert_alpha(),
    pygame.image.load('img/player_right/player-right3.png').convert_alpha(),
    pygame.image.load('img/player_right/player-right4.png').convert_alpha(),
]
#Объявляем параматры игрока
player_x = 680 #Координаты игрока по оси x
player_y = 910 #Координаты игрока по оси y
player_width = 126 #
player_height = 136
player_speed = 15
player_scale = 1  # Увеличение размера игрока в два раза
# Текущая анимация и индекс текущего кадра игрока
current_animation = player_images_right
current_frame_index = 0
last_shoot_time = 0
# Начальные значения для прыжка игрока
is_jumping = False
jump_count = 11
jump_count_new = 13
# Функция отрисовки игрока
def draw_player(x, y):
    current_frame = current_animation[current_frame_index]
    scaled_frame = pygame.transform.scale(current_frame, (player_width * player_scale, player_height * player_scale))
    screen.blit(scaled_frame, (x, y))
    return current_frame
#=====================================================================================================================
#===================================================Блок стрел=========================================================
arrow_right = pygame.image.load('img/arrow_right.png').convert_alpha()
arrow_left = pygame.image.load('img/arrow_left.png').convert_alpha()
arrow_add = pygame.image.load('img/arrow_сounter.png').convert_alpha()
arrow_score = 5
arrow_list_right =[]
arrow_list_left =[]
arrow_add_y =910
arrow_add_list = []
def generate_arrow_time():
    return random.randint(10000, 15000)  # Генерация случайного числа от 5000 до 15000 (в миллисекундах)
arrow_timer = pygame.USEREVENT + 3
arrow_time = generate_arrow_time()
pygame.time.set_timer(arrow_timer, arrow_time)
#======================================================================================================================
#=============================================Блока противников=======================================================
# =============Параметры противника кактус=========================
enemy_cactus = pygame.image.load('img/enemy.png').convert_alpha()
enemy_cactus_y = 860
enemy_cactus_list = []
# =============Параметры противника птица=========================
enemy_bird = pygame.image.load('img/bird.png').convert_alpha()
enemy_bird_y = 700
enemy_bird_list = []
# =============Параметры противника балиста=========================
balista = pygame.image.load('img/ballista.png').convert_alpha()
enemy_balista_y = 930
enemy_balista_list = []
balista_arrow = pygame.image.load('img/balista_arrow.png')
balista_arrow_list =[]
# ========================Создание таймера для генерации врагов=========================
# Функция для генерации случайного времени появления противника
def generate_enemy_time():
    return random.randint(1000, 10000)  # Генерация случайного числа от 1000 до 10000 (в миллисекундах)
#Создание таймера для противника кактус
enemy_cactus_timer = pygame.USEREVENT + 1
enemy_cactus_time = generate_enemy_time()
pygame.time.set_timer(enemy_cactus_timer, enemy_cactus_time)
#Создание таймера для противника птица
enemy_bird_timer = pygame.USEREVENT + 2
enemy_bird_time = generate_enemy_time()
pygame.time.set_timer(enemy_bird_timer, enemy_bird_time)
def generate_balista_time():
    return random.randint(8000, 15000)  # Генерация случайного числа от 8000 до 15000 (в миллисекундах)
# Создание таймера для генерации противника балисты
balista_timer = pygame.USEREVENT + 5
enemy_balista_time = generate_balista_time()
pygame.time.set_timer(balista_timer, enemy_balista_time)
#======================================================================================================================
#==============================================Блок монеток============================================================
# # Загрузка изображения бонусного объекта
coin = pygame.image.load('img/coin.png').convert_alpha()
coin_y = 925
coin_list = []
score_coin = 0
best_score = 0
# Функция для генерации случайного времени появления бонусного объекта
def generate_bonus_time():
    return random.randint(5000, 10000)  # Генерация случайного числа от 5000 до 10000 (в миллисекундах)
# Создание таймера для генерации бонусного объекта
coin_timer = pygame.USEREVENT + 4
coin_time = generate_bonus_time()
pygame.time.set_timer(coin_timer, coin_time)
#=====================================================================================================================
#=============================================Блока Босса=======================================================
# =================================Параметры босса=========================
enemy_boss = pygame.image.load('img/boss.png').convert_alpha()
boss_image_flipped = pygame.transform.flip(enemy_boss, True, False)
enemy_boss_image = enemy_boss
enemy_boss_y = 790
enemy_boss_x = 1980
boss_speed = 6
boss_life = 15
# Добавьте параметр для направления движения босса
boss_direction = 1  # 1 - движение вправо, -1 - движение влево
fireboll_right = pygame.image.load('img/fire_boll_right.png').convert_alpha()
fireboll_left = pygame.image.load('img/fire_boll_left.png').convert_alpha()
fireboll_list_right =[]
fireboll_list_left =[]
#====================================================================================================================
#===========================================Блок настроек запуска игрового процесса====================================
running = True # Флаг работы игры
gameplay = True # Флаг когда идет игровой процесс
gameplay_lite = True# Флаг основной игры
paused = False  # Флаг состояния паузы
boss_active = False # Флаг Босса
game_complite = False # Флаг игра завершена
#==============================================Блок обработки событий в игре===========================================
while running:
    for event in pygame.event.get():  # Обрабатываем события
        if event.type == pygame.KEYDOWN:  # Если нажата кнопка "Закрыть"
            if event.key == pygame.K_ESCAPE:
                running = False  # Завершаем игру
                pygame.quit()  # Завершаем работу pygame
                sys.exit()  # Завершаем программу
            elif event.key == pygame.K_p and gameplay:  # Если нажата кнопка "P"
                paused = not paused  # Переключаем состояние паузы
            if score_coin >= 1 and not boss_active:
                arrow_score = 25
                boss_active = True
                gameplay_lite = False
        current_time = pygame.time.get_ticks()
        #===================== Генрация противника кактуса по таймеру=============================
        if event.type == enemy_cactus_timer and gameplay_lite and not paused:
            enemy_cactus_list.append(enemy_cactus.get_rect(topleft=(window_width, enemy_cactus_y)))
            enemy_cactus_time = generate_enemy_time()
            pygame.time.set_timer(enemy_cactus_timer, enemy_cactus_time)
        #=====================Генрация противника птица по таймеру=============================
        if event.type == enemy_bird_timer and gameplay_lite and not paused:
            enemy_bird_list.append(enemy_bird.get_rect(topleft=(window_width, enemy_bird_y)))
            enemy_bird_time = generate_enemy_time()
            pygame.time.set_timer(enemy_bird_timer, enemy_bird_time)
        # ====================== Генерация противника балиста по таймеру ======================
        if event.type == balista_timer and gameplay_lite and not paused:
            enemy_balista_list.append(balista.get_rect(topleft=(window_width, enemy_balista_y)))
            enemy_balista_time = generate_balista_time()
            pygame.time.set_timer(balista_timer, enemy_balista_time)
            # =========================================================================
# ===================== Генрация стрел для игрока по таймеру==============================
        if event.type == arrow_timer and gameplay_lite and not paused:
            arrow_add_list.append(arrow_add.get_rect(topleft=(window_width + random.randint(200,800), arrow_add_y)))
            arrow_time = generate_arrow_time()
            pygame.time.set_timer(arrow_timer, arrow_time)
        #==============================================================================
        # ===================== Генрация монеток для игрока по таймеру============================
        if event.type == coin_timer and gameplay_lite and not paused:
            coin_list.append(coin.get_rect(topleft=(window_width, coin_y - random.randrange(0, 200, 20))))
            coin_time = generate_bonus_time()
            pygame.time.set_timer(coin_timer, coin_time)
        # ================================================================================
        #===========================Обработка выстрела стрелы игроком======================================
        if gameplay and not paused and event.type == pygame.KEYUP and event.key == pygame.K_SPACE and arrow_score > 0 and current_time - last_shoot_time >= 500:
            if current_animation == player_images_right:
                pygame.mixer.Sound.play(arrow_sound)
                arrow_list_right.append((arrow_right.get_rect(topleft=(player_x + 90, player_y + 50))))
                arrow_score -= 1
            else:
                pygame.mixer.Sound.play(arrow_sound)
                arrow_list_left.append((arrow_left.get_rect(topleft=(player_x - 90, player_y + 50))))
                arrow_score -= 1
            last_shoot_time = current_time
        #=============================================================================================
    # =============================================Игровой процесс======================================================
    if gameplay and not paused:
        # Обновление координат заднего фона
        background_x -= background_speed
        # Проверка, если задний фон вышел за пределы экрана, смещаем его обратно
        if background_x <= -window_width:
            background_x = 0
        screen.fill((0, 0, 0))
        keys = pygame.key.get_pressed()
        # Обработка движения игрока
        if keys[pygame.K_LEFT]:
            current_animation = player_images_left
            player_x -= player_speed
        elif keys[pygame.K_RIGHT]:
            current_animation = player_images_right
            player_x += player_speed
        # Ограничение игрока в пределах экрана
        if player_x < 0:
            player_x = 0
        elif player_x > window_width - player_width * player_scale:
            player_x = window_width - player_width * player_scale
        # Очистка экрана
        screen.fill((0, 0, 0))
        # Отрисовка заднего фона
        draw_background(background_x, background_y)
        # Отрисовка игрока
        draw_player(player_x, player_y)
        # Отрисовка счетчика стрел
        arrow_label = font_arrow.render(f'{arrow_score}', False, (255,255,255))
        screen.blit(arrow_counter,(20,110))
        screen.blit(arrow_label,(120,125))
        # Отрисовка счетчика монет
        coin_label = font_coin.render(f'{score_coin}', False, (255,255,255))
        screen.blit(coin_counter, (20, 20 ))
        screen.blit(coin_label, (120, 25 ))
        # Отрисовка лучшего счета
        best_score_label = font_best_score.render(f'{best_score}', False, (255,255,255))
        screen.blit(best_score_image, (860, 20))
        screen.blit(best_score_label, (960, 25))
        # Обновление индекса текущего кадра анимации
        current_frame_index = (current_frame_index + 1) % len(current_animation)
        player_rect = player_images_right[0].get_rect(topleft=(player_x, player_y))
        # ===================Обработка подбор стрел игроком====================
        if arrow_add_list:
            for (i, arrow_add_rect) in enumerate(arrow_add_list):
                screen.blit(arrow_add, arrow_add_rect)
                arrow_add_rect.x -= 4
                if arrow_add_rect.x < -100:
                    arrow_add_list.pop(i)
                if player_rect.colliderect(arrow_add_rect):
                    pygame.mixer.Sound.play(arrow_sound_add)
                    arrow_score += 2
                    arrow_add_list.pop(i)
        # ================================================================
        # ===================Обработка подбора монеток====================
        if coin_list:
            for (i, coin_rect) in enumerate(coin_list):
                screen.blit(coin, coin_rect)
                coin_rect.x -= 4
                if coin_rect.x < -100:
                    coin_list.pop(i)
                if player_rect.colliderect(coin_rect):
                    pygame.mixer.Sound.play(add_coin)
                    score_coin += 1
                    coin_list.pop(i)
        # =================================================================
        if gameplay_lite:
            # =========================Обработка стрелы игрока летящей вправо==========================
            if arrow_list_right:
                for (i, arrow_rect_right) in enumerate(arrow_list_right):
                    screen.blit(arrow_right, (arrow_rect_right.x, arrow_rect_right.y))
                    arrow_rect_right.x += 5
                    if arrow_rect_right.x > window_width:
                        arrow_list_right.pop(i)
                    if arrow_rect_right.x > window_width:
                        arrow_list_right.pop(i)
                    if enemy_cactus_list:
                        for (index, enemy_rect_cactus) in enumerate(enemy_cactus_list):
                            if arrow_rect_right.colliderect(enemy_rect_cactus):
                                pygame.mixer.Sound.play(enemy_hit)
                                enemy_cactus_list.pop(index)
                                arrow_list_right.pop(i)
                    if enemy_bird_list:
                        for (index, enemy_rect_bird) in enumerate(enemy_bird_list):
                            if arrow_rect_right.colliderect(enemy_rect_bird):
                                pygame.mixer.Sound.play(enemy_hit)
                                enemy_bird_list.pop(index)
                                arrow_list_right.pop(i)
                    if enemy_balista_list:
                        for (index, enemy_rect_balista) in enumerate(enemy_balista_list):
                            if arrow_rect_right.colliderect(enemy_rect_balista):
                                pygame.mixer.Sound.play(enemy_hit)
                                arrow_add_list.append(
                                    arrow_add.get_rect(topleft=(enemy_rect_balista.x, arrow_add_y)))
                                enemy_balista_list.pop(index)
                                arrow_list_right.pop(i)
                    if balista_arrow_list:
                        for (index, balista_arrow_rect) in enumerate(balista_arrow_list):
                            if arrow_rect_right.colliderect(balista_arrow_rect):
                                pygame.mixer.Sound.play(enemy_hit)
                                balista_arrow_list.pop(index)
                                arrow_list_right.pop(i)
            # ========================================================================================
            # =========================Обработка стрелы игрока летящей влево==========================
            if arrow_list_left:
                for (i, arrow_rect_left) in enumerate(arrow_list_left):
                    screen.blit(arrow_left, (arrow_rect_left.x, arrow_rect_left.y))
                    arrow_rect_left.x -= 9
                    if arrow_rect_left.x > window_width:
                        arrow_list_left.pop(i)
                    if enemy_cactus_list:
                        for (index, enemy_rect_cactus) in enumerate(enemy_cactus_list):
                            if arrow_rect_left.colliderect(enemy_rect_cactus):
                                pygame.mixer.Sound.play(enemy_hit)
                                enemy_cactus_list.pop(index)
                                arrow_list_left.pop(i)
                    if enemy_bird_list:
                        for (index, enemy_rect_bird) in enumerate(enemy_bird_list):
                            if arrow_rect_left.colliderect(enemy_rect_bird):
                                pygame.mixer.Sound.play(enemy_hit)
                                enemy_bird_list.pop(index)
                                arrow_list_left.pop(i)
                    if enemy_balista_list:
                        for (index, enemy_rect_balista) in enumerate(enemy_balista_list):
                            if arrow_rect_left.colliderect(enemy_rect_balista):
                                pygame.mixer.Sound.play(enemy_hit)
                                enemy_balista_list.pop(index)
                                arrow_list_left.pop(i)
                    if balista_arrow_list:
                        for (index, balista_arrow_rect) in enumerate(balista_arrow_list):
                            if arrow_rect_left.colliderect(balista_arrow_rect):
                                pygame.mixer.Sound.play(enemy_hit)
                                balista_arrow_list.pop(index)
                                arrow_list_left.pop(i)
            # Обработка прыжка игрока
            if not is_jumping:
                if keys[pygame.K_UP]:
                    is_jumping = True
                    pygame.mixer.Sound.play(jump_sound)
            else:
                if jump_count >= -11:
                    neg = 1
                    if jump_count < 0:
                        neg = -1
                    player_y -= (jump_count ** 2) * 0.5 * neg
                    jump_count -= 1
                else:
                    is_jumping = False
                    jump_count = 11
            # ===================Обработка противника кактус========================
            if enemy_cactus_list:
                for (i, enemy_cactus_rect) in enumerate(enemy_cactus_list):
                    screen.blit(enemy_cactus, enemy_cactus_rect)
                    enemy_cactus_rect.x -= 4
                    if enemy_cactus_rect.x < -100:
                        enemy_cactus_list.pop(i)
                    if player_rect.colliderect(enemy_cactus_rect):
                        pygame.mixer.Sound.play(player_loss)
                        gameplay = False
            # ===================================================================
            # ====================Обработка противника птица========================
            if enemy_bird_list:
                for (a, enemy_bird_rect) in enumerate(enemy_bird_list):
                    screen.blit(enemy_bird, enemy_bird_rect)
                    enemy_bird_rect.x -= 7
                    if enemy_bird_rect.x < -100:
                        enemy_bird_list.pop(a)
                    if player_rect.colliderect(enemy_bird_rect):
                        pygame.mixer.Sound.play(player_loss)
                        gameplay = False
            # ================================================================
            # ===================Обработка противника балиста========================
            if enemy_balista_list:
                for enemy_balista_rect in enemy_balista_list:
                    screen.blit(balista, enemy_balista_rect)
                    enemy_balista_rect.x -= 4
                    if enemy_balista_rect.x < -200:
                        enemy_balista_list.remove(enemy_balista_rect)
                    if player_rect.colliderect(enemy_balista_rect):
                        pygame.mixer.Sound.play(player_loss)
                        gameplay = False
                    # Создание новой стрелы для каждой балисты
                    if random.randint(0, 120) < 1:  # Вероятность выстрела турели
                        pygame.mixer.Sound.play(arrow_balista_sound)
                        balista_arrow_list.append(balista_arrow.get_rect(
                            topleft=(enemy_balista_rect.x, enemy_balista_rect.y + 10)))
                    # =========================================================================
                    # =========================Обработка стрелы балиста========================
                    if balista_arrow_list:
                        for (i, balista_arrow_rect) in enumerate(balista_arrow_list):
                            screen.blit(balista_arrow, (balista_arrow_rect.x, balista_arrow_rect.y))
                            balista_arrow_rect.x -= 9
                            if balista_arrow_rect.colliderect(player_rect):
                                pygame.mixer.Sound.play(player_loss)
                                gameplay = False
                                break
                            if balista_arrow_rect.x < -100:
                                balista_arrow_list.pop(i)
                    # =========================================================================
        # =======================Игровой процесс с Боссом========================================================
        if boss_active:
            # =========================Обработка стрелы игрока летящей вправо==========================
            if arrow_list_right:
                for (i, arrow_rect_right) in enumerate(arrow_list_right):
                    screen.blit(arrow_right, (arrow_rect_right.x, arrow_rect_right.y))
                    arrow_rect_right.x += 5
                    if arrow_rect_right.x > window_width:
                        arrow_list_right.pop(i)
                    if arrow_rect_right.x > window_width:
                        arrow_list_right.pop(i)
                    if arrow_rect_right.colliderect(enemy_boss_rect):
                        pygame.mixer.Sound.play(enemy_hit)
                        boss_life -= 1
                        if boss_life == 0:
                            pygame.mixer.music.stop()
                            pygame.mixer.Sound.play(game_complite_sound)
                            game_complite = True
                            gameplay = False
                        arrow_list_right.pop(i)
                    if fireboll_list_right:
                        for (index, fireboll_right_rect) in enumerate(fireboll_list_right):
                            if arrow_rect_right.colliderect(fireboll_right_rect):
                                pygame.mixer.Sound.play(enemy_hit)
                                fireboll_list_right.pop(index)
                                arrow_list_right.pop(i)
                    if fireboll_list_left:
                        for (index, fireboll_right_rect) in enumerate(fireboll_list_left):
                            if arrow_rect_right.colliderect(fireboll_left_rect):
                                pygame.mixer.Sound.play(enemy_hit)
                                fireboll_list_left.pop(index)
                                arrow_list_right.pop(i)
            # ========================================================================================
            # =========================Обработка стрелы игрока летящей влево==========================
            if arrow_list_left:
                for (i, arrow_rect_left) in enumerate(arrow_list_left):
                    screen.blit(arrow_left, (arrow_rect_left.x, arrow_rect_left.y))
                    arrow_rect_left.x -= 9
                    if arrow_rect_left.x > window_width:
                        arrow_list_left.pop(i)
                    if arrow_rect_left.x > window_width:
                        arrow_list_left.pop(i)
                    if arrow_rect_left.colliderect(enemy_boss_rect):
                        pygame.mixer.Sound.play(enemy_hit)
                        boss_life -= 1
                        if boss_life == 0:
                            pygame.mixer.music.stop()
                            pygame.mixer.Sound.play(game_complite_sound)
                            game_complite = True
                            gameplay = False
                        arrow_list_left.pop(i)
                    if fireboll_list_right:
                        for (index, fireboll_right_rect) in enumerate(fireboll_list_right):
                            if arrow_rect_left.colliderect(fireboll_right_rect):
                                pygame.mixer.Sound.play(enemy_hit)
                                fireboll_list_right.pop(index)
                                arrow_list_left.pop(i)
                    if fireboll_list_left:
                        for (index, fireboll_right_rect) in enumerate(fireboll_list_left):
                            if arrow_rect_left.colliderect(fireboll_left_rect):
                                pygame.mixer.Sound.play(enemy_hit)
                                fireboll_list_left.pop(index)
                                arrow_list_left.pop(i)
            # Обработка прыжка игрока
            if not is_jumping:
                if keys[pygame.K_UP]:
                    is_jumping = True
                    pygame.mixer.Sound.play(jump_sound)
            else:
                if jump_count_new >= -13:
                    neg = 1
                    if jump_count_new < 0:
                        neg = -1
                    player_y -= (jump_count_new ** 2) * 0.5 * neg
                    jump_count_new -= 1
                else:
                    is_jumping = False
                    jump_count_new = 13
            enemy_boss_x += boss_speed * boss_direction
            screen.blit(enemy_boss_image, (enemy_boss_x, enemy_boss_y))
            enemy_boss_rect = enemy_boss_image.get_rect(
                topleft=(enemy_boss_x, enemy_boss_y))
            if enemy_boss_x <= 0:
                boss_direction = 1  # Измените направление на движение вправо
                boss_speed = 3
                enemy_boss_image = enemy_boss
            elif enemy_boss_x >= window_width - enemy_boss.get_width():
                boss_direction = -1  # Измените направление на движение влево
                boss_speed = 6
                enemy_boss_image = boss_image_flipped
            if random.randint(0, 120) < 2:  # Вероятность выстрела Босса
                pygame.mixer.Sound.play(arrow_balista_sound)
                # =========================Генерация огненого шара вправо========================
                if enemy_boss_image == enemy_boss:
                    pygame.mixer.Sound.play(fireboll_sound)
                    fireboll_list_right.append(fireboll_right.get_rect(topleft=(
                    enemy_boss_x + 90,
                    enemy_boss_y + random.randrange(50, 150, 10))))
                # =========================Генерация огненого шара влево========================
                if enemy_boss_image == boss_image_flipped:
                    pygame.mixer.Sound.play(fireboll_sound)
                    fireboll_list_left.append(fireboll_left.get_rect(topleft=(
                    enemy_boss_x - 90,
                    enemy_boss_y + random.randrange(50, 150, 10))))
            # =========================Обработка огненого шара влево========================
            if fireboll_list_left:
                for (i, fireboll_left_rect) in enumerate(fireboll_list_left):
                    screen.blit(fireboll_left,
                                (fireboll_left_rect.x, fireboll_left_rect.y))
                    fireboll_left_rect.x -= 9
                    if fireboll_left_rect.colliderect(player_rect):
                        pygame.mixer.Sound.play(player_loss)
                        gameplay = False
                        boss_active = False
                        break
                    if fireboll_left_rect.x < -100:
                        fireboll_list_left.pop(i)
            # =========================Обработка огненого шара вправо========================
            if fireboll_list_right:
                for (i, fireboll_right_rect) in enumerate(fireboll_list_right):
                    screen.blit(fireboll_right,
                                (fireboll_right_rect.x, fireboll_right_rect.y))
                    fireboll_right_rect.x += 5
                    if fireboll_right_rect.colliderect(player_rect):
                        pygame.mixer.Sound.play(player_loss)
                        gameplay = False
                        boss_active = False
                        break
                    if fireboll_right_rect.x < -100:
                        fireboll_list_right.pop(i)
            # ========================Обработка столкновения с боссом=======================================
            if player_rect.colliderect(enemy_boss_rect):
                pygame.mixer.Sound.play(player_loss)
                gameplay = False
                # ================================================================================================
    # ============================================Экрана паузы========================================================
    elif paused:
        pause_label1 = font_gameover.render('PAUSE', False,
                            (182, 165, 20))
        pause_label2 = font_gameover.render('PAUSE', False,
                            (248, 228, 63))
        screen.blit(pause_label1, (745, 185))
        screen.blit(pause_label2, (740, 180))
        # ===================================================================================================================
        # ============================================Блок проигрыша========================================================
    elif not gameplay and not paused and not game_complite:
        screen.fill('black')
        screen.blit(gameover_label, (640, 380))
        screen.blit(restart_label, (530, 650))
        coin_label = font_coin.render(f'{score_coin}', False, 'white')
        screen.blit(coin_counter, (910, 520))
        screen.blit(coin_label, (1010, 525))
        key_gameover = pygame.key.get_pressed()
        if key_gameover[pygame.K_r]:
            player_x = 680
            player_y = 910
            jump_count = 11
            current_animation = player_images_right
            enemy_cactus_list.clear()
            enemy_bird_list.clear()
            enemy_balista_list.clear()
            balista_arrow_list.clear()
            arrow_list_right.clear()
            arrow_list_left.clear()
            arrow_add_list.clear()
            coin_list.clear()
            fireboll_list_right.clear()
            fireboll_list_left.clear()
            arrow_score = 5
            if score_coin > best_score:
                best_score = score_coin
            score_coin = 0
            gameplay = True
            gameplay_lite = True
            boss_active = False
    elif game_complite:
        screen.blit(background_endgame, (0, 0))
        game_complite_label1 = font_gameover.render('Поздравляем!',
                                    False,
                                    (182, 165, 20))
        game_complite_label2 = font_gameover.render('Поздравляем!',
                                    False,
                                    (248, 228, 63))
        screen.blit(game_complite_label1, (535, 185))
        screen.blit(game_complite_label2, (530, 180))
        game_complite_label3 = font_gameover.render('Вы прошли игру!',
                                    False,
                                    (182, 165, 20))
        game_complite_label4 = font_gameover.render('Вы прошли игру!',
                                    False,
                                    (248, 228, 63))
        screen.blit(game_complite_label3, (425, 385))
        screen.blit(game_complite_label4, (420, 380))
        game_complite_label5 = font_arrow.render(
            'Ждите новых обновлений,', False, (182, 165, 20))
        game_complite_label6 = font_arrow.render(
            'Ждите новых обновлений,', False, (248, 228, 63))
        screen.blit(game_complite_label5, (315, 585))
        screen.blit(game_complite_label6, (313, 580))
        game_complite_label5 = font_arrow.render(
            'скоро появится много нового!', False, (182, 165, 20))
        game_complite_label6 = font_arrow.render(
            'скоро появится много нового!', False, (248, 228, 63))
        screen.blit(game_complite_label5, (125, 685))
        screen.blit(game_complite_label6, (123, 680))
        # ======================================================================================================================
    pygame.display.update()
    # ===================================================================================================================
    clock.tick(45)  # Устанавливаем частоту обновления экрана