import pygame, time, random

pygame.init()

pygame.display.set_caption("Mi Primer Juego")

screen_h = 849
screen_v = 565
white = (255, 255, 255)
screen = pygame.display.set_mode([screen_h, screen_v])

clock = pygame.time.Clock()

font = pygame.font.Font(None, 60)

speed_x = 2
speed_y = 2

ball_sound= pygame.mixer.Sound("patada_balon.mp3")
bg_music= pygame.mixer.Sound("musica_epica.mp3")

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("bola pygame.png").convert()
        self.image.set_colorkey(white)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, speed_x=2, speed_y=2):
        super().__init__()
        self.image = pygame.image.load("jugador pygame.png").convert()
        self.image.set_colorkey(white)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.target = (random.randint(0, 702), random.randint(0, 397))
        self.move_timer = time.time()
        self.speed_x = speed_x
        self.speed_y = speed_y


    def update(self):
        current_time = time.time()
        
        self.speed_x=speed_x
        self.speed_y=speed_y
        
        if current_time - self.move_timer > 10:
            self.target = (random.randint(0, 702), random.randint(0, 397))
            self.move_timer = current_time

        target_x, target_y = self.target

        if self.rect.x == target_x and self.rect.y == target_y:
            self.target = (random.randint(0, 702), random.randint(0, 397))

        if self.rect.x - target_x >= -self.speed_x and self.rect.x - target_x <= self.speed_x:
            self.speed_x = abs(self.rect.x - target_x)

        if self.rect.y - target_y >= -self.speed_y and self.rect.y - target_y <= self.speed_y:
            self.speed_y = abs(self.rect.y - target_y)

        if self.rect.x < target_x:
            self.rect.x += self.speed_x
        elif self.rect.x > target_x:
            self.rect.x -= self.speed_x

        if self.rect.y < target_y:
            self.rect.y += self.speed_y
        elif self.rect.y > target_y:
            self.rect.y -= self.speed_y

class Button:
    def __init__(self, text, pos, font, bg="black", feedback=""):
        self.x, self.y = pos
        self.font = pygame.font.Font(None, font)
        self.feedback = feedback
        if feedback == "":
            self.feedback = text
        self.change_text(text, bg)

    def change_text(self, text, bg="black"):
        self.text = self.font.render(text, True, pygame.Color("White"))
        self.size = self.text.get_size()
        self.surface = pygame.Surface(self.size)
        self.surface.fill(bg)
        self.surface.blit(self.text, (0, 0))
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])

    def show(self, screen):
        screen.blit(self.surface, (self.x, self.y))

    def click(self, event):
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if self.rect.collidepoint(x, y):
                    return True
        return False

def menu(final_time=None):
    pygame.mouse.set_visible(True)
    
    menu_font = pygame.font.Font(None, 100)
    menu_text = menu_font.render("Esquiva Patadas", True, (255, 255, 255))

    screen.fill((0, 0, 0))
    screen.blit(menu_text, (screen_h // 2 - menu_text.get_width() // 2, screen_v // 3))

    if final_time is not None:
        time_text = font.render(f"Tiempo Final: {final_time:02}", True, (255, 255, 255))
        screen.blit(time_text, (screen_h // 2 - time_text.get_width() // 2, 50))

    start_button = Button("Jugar", (screen_h // 2 - 100, screen_v // 2), 60)
    settings_button = Button("Ajustes", (screen_h // 2 - 100, screen_v // 2 + 80), 60)
    quit_button = Button("Cerrar", (screen_h // 2 - 100, screen_v // 2 + 160), 60)
    
    start_button.show(screen)
    settings_button.show(screen)
    quit_button.show(screen)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if start_button.click(event):
                waiting = False
                game()
            if settings_button.click(event):
                settings()
            if quit_button.click(event):
                pygame.quit()
                exit()

def settings():
    pygame.mouse.set_visible(True)
    
    settings_font = pygame.font.Font(None, 60)
    settings_text = settings_font.render("Menú de Ajustes", True, (255, 255, 255))
    screen.fill((0, 0, 0))
    screen.blit(settings_text, (screen_h // 2 - settings_text.get_width() // 2, 50))
    
    back_button = Button("Volver", (screen_h // 2 - 100, screen_v // 2 + 160), 60)
    volume_button = Button("Volumen", (screen_h // 2 - 100, screen_v // 2), 60)
    dificulty_button = Button("Dificultad", (screen_h // 2 - 100, screen_v // 2 + 80), 60)
    
    back_button.show(screen)
    volume_button.show(screen)
    dificulty_button.show(screen)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if back_button.click(event):
                waiting = False
                menu()
            if volume_button.click(event):
                waiting = False
                menu()
            if dificulty_button.click(event):
                waiting = False
                dificulty()

def dificulty():
    pygame.mouse.set_visible(True)
    global speed_y, speed_x
    dificulty_font = pygame.font.Font(None, 60)
    dificulty_text = dificulty_font.render("Dificultad", True, (255, 255, 255))
    screen.fill((0, 0, 0))
    screen.blit(dificulty_text, (screen_h // 2 - dificulty_text.get_width() // 2, 50))
    
    back_button = Button("Volver", (screen_h // 2 - 100, screen_v // 2 + 160), 60)
    easy_button = Button("Fácil", (screen_h // 2 - 100, screen_v // 2 - 80), 60)
    mid_button = Button("Medio", (screen_h // 2 - 100, screen_v // 2), 60)
    dificult_button = Button("Difícil", (screen_h // 2 - 100, screen_v // 2 + 80), 60)
    
    back_button.show(screen)
    easy_button.show(screen)
    mid_button.show(screen)
    dificult_button.show(screen)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if back_button.click(event):
                waiting = False
                settings()
            if easy_button.click(event):
                waiting = False
                speed_x = 2
                speed_y = 2
                menu()
            if mid_button.click(event):
                waiting = False
                speed_x = 4
                speed_y = 4
                menu()
            if dificult_button.click(event):
                waiting = False
                speed_x = 6
                speed_y = 6
                menu()

def game():
    pygame.mouse.set_visible(False)
    bg_music.play(-1)
    start_time = time.time()

    player = Player()
    enemy = Enemy(speed_x, speed_y)
    enemy2 = Enemy(speed_x, speed_y)
    enemy3 = Enemy(speed_x, speed_y)
    enemy4 = Enemy(speed_x, speed_y)
    enemy5 = Enemy(speed_x, speed_y)

    player.rect.center = (screen_h // 2, screen_v // 2)
    enemy.rect.center = (-100, -100)
    enemy2.rect.center = (900, 600)
    enemy3.rect.center = (900, -100)
    enemy4.rect.center = (-100, 600)
    enemy5.rect.center = (425, 600)

    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    all_sprites.add(enemy)
    all_sprites.add(enemy2)
    all_sprites.add(enemy3)
    all_sprites.add(enemy4)
    all_sprites.add(enemy5)

    enemy_list = pygame.sprite.Group()
    enemy_list.add(enemy)
    enemy_list.add(enemy2)
    enemy_list.add(enemy3)
    enemy_list.add(enemy4)
    enemy_list.add(enemy5)

    dead_list = pygame.sprite.Group()

    background = pygame.image.load("background pygame.jpg").convert()

    game_over = False
    collision_occurred = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        if not collision_occurred:
            elapsed_time = time.time() - start_time
            minutes = int(elapsed_time // 60)
            seconds = int(elapsed_time % 60)
            centiseconds = int((elapsed_time * 100) % 100)
            timer_text = font.render(f"{minutes:02}:{seconds:02}:{centiseconds:02}", True, (255, 255, 255))
        else:
            timer_text = font.render(f"{minutes:02}:{seconds:02}:{centiseconds:02}", True, (255, 255, 255))

        mouse_coords = pygame.mouse.get_pos()
        if mouse_coords[0] > 0:
            player.rect.center = mouse_coords

        if not collision_occurred:
            enemy_list.update()

        for enemy in enemy_list:
            if pygame.sprite.collide_mask(player, enemy):
                dead_list.add(player)
                all_sprites.remove(player)
                ball_sound.play()
                bg_music.stop()
                collision_occurred = True
                game_over = True

        screen.blit(background, [0, 0])
        all_sprites.draw(screen)
        screen.blit(timer_text, (655, 0))
        pygame.display.flip()

        clock.tick(60)

    final_time = f"{minutes:02}:{seconds:02}:{centiseconds:02}"
    menu(final_time)

menu()
pygame.quit()
exit()