import pygame
import random
import sys
from math import sqrt, atan2, degrees

pygame.init()
size = width, height = 900, 700
fps = 120
screen = pygame.display.set_mode(size)


def start_screen():
    intro_text = ["AD - движение влево/вправо",
                  "Пробел - прыжок",
                  "ЛКМ - выстрел",
                  "P - пауза",
                  "F1 - полноэкранный режим",
                  "Нажмите на любую клавишу, чтобы продолжить."]
    screen.fill((0, 0, 0))

    title = pygame.font.Font(None, int(120 / 700 * height)).render('Cave Explorer', 1, (255, 0, 0))
    screen.blit(title, ((width - title.get_rect().width) // 2, int(200 / 700 * height)))
  
    font = pygame.font.Font(None, int(30 / 700 * height))
    text_coord = int(200 / 700 * height) + title.get_rect().bottom
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += int(10 / 600 * width)
        intro_rect.top = text_coord
        intro_rect.x = (width - string_rendered.get_rect().width) // 2
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    color = [255, 0, 0]
    cycle = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        if cycle == 0:
            color[0] -= 1
            color[1] += 1
            if color == [0, 255, 0]:
                cycle = 1
        elif cycle == 1:
            color[1] -= 1
            color[2] += 1
            if color == [0, 0, 255]:
                cycle = 2
        elif cycle == 2:
            color[2] -= 1
            color[0] += 1
            if color == [255, 0, 0]:
                cycle = 0
        title = pygame.font.Font(None, int(120 / 700 * height)).render('Cave Explorer', 1, color)
        screen.blit(title, ((width - title.get_rect().width) // 2, int(200 / 700 * height)))
            
        pygame.display.flip()
        clock.tick(fps)


def gameover_screen(score):
    screen.fill((0, 0, 0))
    intro_text = ['Нажмите на кнопку "Escape", чтобы выйти из игры',
                  "R - начать заново", "",
                  "Ваш счёт - {}".format(str(score // 120))]
    title = pygame.font.Font(None, 120).render('Игра окончена.', 1, pygame.Color('white'))
    screen.blit(title, ((width - title.get_rect().width) // 2, 200))
    font = pygame.font.Font(None, 30)
    text_coord = 200 + title.get_rect().bottom
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = (width - string_rendered.get_rect().width) // 2
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    idle = True
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    raise SystemExit
                elif idle and event.key == pygame.K_r:
                    start()
            
            
        pygame.display.flip()
        clock.tick(fps)

    
def rng(chance):
    cap = 100
    if type(chance) == float:
        while int(chance) != chance:
            chance *= 10
            cap *= 10
    return True if random.randint(1, cap) <= chance else False


def rotatePivoted(im, angle, pivot):
    image = pygame.transform.rotate(im, angle)
    rect = image.get_rect()
    rect.center = pivot
    return image, rect

            
####################################################################################

            
def start():
    players = pygame.sprite.Group()
    melee_enemies = pygame.sprite.Group()
    ranged_enemies = pygame.sprite.Group()
    background = pygame.sprite.Group()
    ground = pygame.sprite.Group()
    platforms = pygame.sprite.Group()
    projectiles = pygame.sprite.Group()
    enemy_projectiles = pygame.sprite.Group()
    explosions = pygame.sprite.Group()
    enemy_explosions = pygame.sprite.Group()
    decorations = pygame.sprite.Group()
    foreground = pygame.sprite.Group()


    class Ground(pygame.sprite.Sprite):
        def __init__(self, group, size, color, x, y):
            super().__init__(group)
            self.below_player = False
            self.image = pygame.Surface(size,
                                        pygame.SRCALPHA, 32)
            pygame.draw.rect(self.image, color,
                               (0, 0, size[0], size[1]))
            self.rect = pygame.Rect(x, y, size[0], size[1])
            self.mask = pygame.mask.from_surface(self.image)

        def update(self):
            self.rect = self.rect.move(-speed, 0)
            if pl.rect.bottom <= self.rect.top:
                self.below_player = True
            else:
                self.below_player = False
            if self.rect.right < 0:
                self.kill()

    class Stalactite(pygame.sprite.Sprite):
        def __init__(self, group, x, y, length, color, multiplier, upside_down, outline_color=None):
            super().__init__(group)
            self.length = length
            self.cooldown = 0
            if multiplier < 1:
                self.multiplier = 1
                self.max_cooldown = 1 // multiplier
            else:
                self.multiplier = multiplier
                self.max_cooldown = 0
            self.height = random.randint(length // 1.5, round(length * 1.5))
            self.image = pygame.Surface((length, height))
            self.image.set_colorkey((0, 0, 0))
            if not upside_down:
                pygame.draw.polygon(self.image, color, ((0, 0), (length // 2, self.height), (length, 0)))
                if outline_color is not None:
                    pygame.draw.polygon(self.image, outline_color, ((0, 0), (length // 2, self.height), (length, 0)), 1)
            else:
                pygame.draw.polygon(self.image, color, ((0, self.height), (length // 2, 0), (length, self.height)))
                if outline_color is not None:
                    pygame.draw.polygon(self.image, outline_color, ((0, self.height), (length // 2, 0), (length, self.height)), 1)
            if upside_down:
                self.rect = pygame.Rect(x, y - self.height, length, self.height)
            else:
                self.rect = pygame.Rect(x, y, length, self.height)
            
        def move(self, xvelocity):
            self.rect = self.rect.move(xvelocity, 0)
            
        def update(self):
            if self.cooldown == 0:
                self.move(-speed * self.multiplier)
                if self.rect.right < 0:
                    self.kill()
                self.cooldown = self.max_cooldown
            else:
                self.cooldown -= 1

            
    class Player(pygame.sprite.Sprite):
        def __init__(self, group, x, y):
            super().__init__(group)
            self.on_ground = False
            self.cooldown = 0
            self.xvel = 0
            self.yvel = 0
            self.direction = 0
            self.image = pygame.Surface((34, 36))
            self.image.set_colorkey((0, 0, 0))
            pygame.draw.rect(self.image, pygame.Color("blue"),
                             (7, 0, 20, 36))
            self.gun = pygame.Surface((28, 8),
                                      pygame.SRCALPHA, 32)
            pygame.draw.rect(self.gun, pygame.Color('red'),
                             (8, 0, 20, 8))
            self.image.blit(self.gun, (17, 15))
            self.rect = pygame.Rect(x, y, 20,  36)
            self.mask = pygame.mask.from_surface(self.image)
            
        def move(self, xvelocity, yvelocity):
            self.rect = self.rect.move(xvelocity, yvelocity)

    
    class Projectile(pygame.sprite.Sprite):
        def __init__(self, group, x, y, rotation, velocity, color):
            super().__init__(group)
            self.friendly = self in projectiles
            self.color = color
            self.xremainder = 0
            self.yremainder = 0
            self.image = pygame.Surface((14, 8))
            self.image.set_colorkey((0, 0, 0))
            pygame.draw.polygon(self.image, color, ((0, 0), (14, 4), (0, 8)))
            pygame.draw.polygon(self.image, (0, 0, 0), ((0, 0), (14, 4), (0, 8)), 1)
            self.image = pygame.transform.rotate(self.image, rotation)
            self.rect = pygame.Rect(x, y, 14, 8)
            self.mask = pygame.mask.from_surface(self.image)
            self.velx = velocity[0]
            self.vely = velocity[1]
            if self.friendly:
                self.velx *= 2.5
                self.vely *= 2.5
                pl.cooldown = 30
                pl.xvel -= velocity[0] * 1.7
                pl.yvel -= velocity[1] * 2
                if pl.yvel <= 0 and pl.on_ground:
                    pl.on_ground = False
            else:
                self.velx /= 2
                self.vely /= 2
        def move(self):
            self.rect = self.rect.move(self.velx + self.xremainder, self.vely + self.yremainder)
            self.xremainder = self.velx + self.xremainder - int(self.velx + self.xremainder)
            self.yremainder = self.vely + self.yremainder - int(self.vely + self.yremainder)

        def explode(self):
            if self.friendly:
                Explosion(explosions, self.rect.x, self.rect.y, 30)
            else:
                Enemy_explosion(explosions, self.rect.x, self.rect.y, self.color, 12, 3)
            self.kill()

        def update(self):
            self.move()
            if self.friendly:
                for enemy in ranged_enemies:
                    if pygame.sprite.collide_mask(self, enemy) and enemy.active and not enemy.fading:
                        self.explode()
                        break
                for enemy in melee_enemies:
                    if pygame.sprite.collide_mask(self, enemy) and enemy.active and not enemy.fading:
                        enemy.fading = True
                        self.explode()
                        break
                else:
                    if pygame.sprite.spritecollideany(self, ground) or pygame.sprite.spritecollideany(self, platforms):
                        self.explode()
            else:
                if pygame.sprite.spritecollideany(self, ground) or pygame.sprite.spritecollideany(self, platforms):
                    self.explode()
                if pygame.sprite.collide_mask(self, pl):
                    gameover_screen(score)
                
            if self.rect.x < -10:
                self.kill()

            if self.rect.x > width + 10:
                self.kill()


    class Explosion(pygame.sprite.Sprite):
        def __init__(self, group, x, y, radius):
            super().__init__(group)
            self.stage = 0
            self.radius = radius
            self.image = pygame.Surface((radius * 2, radius * 2))
            self.image.set_colorkey((0, 0, 0))
            self.rect = pygame.Rect(x - radius, y - radius, radius * 2,  radius * 2)
            self.mask = pygame.mask.from_surface(self.image)

        def draw_yellow(self):
            self.image.fill((0, 0, 0))
            pygame.draw.circle(self.image, (255, 255, 0), (self.radius, self.radius), int(self.radius / 3))

        def draw_orange(self):
            self.image.fill((0, 0, 0))
            pygame.draw.circle(self.image, (255, 255, 0), (self.radius, self.radius), int(self.radius / 3))
            pygame.draw.circle(self.image, (255, 165, 0), (self.radius, self.radius), int(self.radius // 3 * 2), int(self.radius // 3))

        def draw_red(self):
            self.image.fill((0, 0, 0))
            pygame.draw.circle(self.image, (255, 255, 0), (self.radius, self.radius), int(self.radius / 3))
            pygame.draw.circle(self.image, (255, 165, 0), (self.radius, self.radius), int(self.radius // 3 * 2), int(self.radius // 3))
            pygame.draw.circle(self.image, (255, 0, 0), (self.radius, self.radius), int(self.radius), int(self.radius // 3))
            
        def update(self):
            if self.stage == 0:
                self.draw_yellow()
            elif self.stage == 5:
                self.draw_orange()
            elif self.stage == 10:
                self.draw_red()
            elif self.stage == 15:
                self.draw_orange()
            elif self.stage == 20:
                self.draw_yellow()
            elif self.stage == 25:
                self.kill()
            self.stage += 1
            for enemy in ranged_enemies:
                if pygame.sprite.collide_circle(self, enemy) and enemy.active and not enemy.fading:
                    enemy.fading = True
            for enemy in melee_enemies:
                if pygame.sprite.collide_circle(self, enemy) and enemy.active and enemy.vulnerable and not enemy.fading:
                    enemy.fading = True


    class Gunner(pygame.sprite.Sprite):
        def __init__(self, group, x, y, initial_cooldown, ccd, fire_delay, max_rockets, color):
            super().__init__(group)
            self.active = False
            self.fading = False
            self.color = color
            self.initial_cooldown = initial_cooldown
            self.const_cooldown = ccd
            self.cooldown = initial_cooldown // 4
            self.fire_delay = fire_delay
            self.release_cooldown = 0
            self.max_rockets = max_rockets
            self.rockets = 0
            self.image = pygame.Surface((40, 40))
            self.image.set_colorkey((0, 0, 0))
            pygame.draw.circle(self.image, color, (20, 20), 14)
            pygame.draw.circle(self.image, (0, 0, 0), (20, 20), 16, 2)
            self.gun = pygame.Surface((40, 8), pygame.SRCALPHA, 32)
            pygame.draw.rect(self.gun, color, (1, 0, 14, 8))
            pygame.draw.rect(self.gun, (0, 0, 0), (1, 0, 14, 8), 1)
            self.image.blit(self.gun, (0, 16))
            self.image.set_alpha(127)
            self.rect = pygame.Rect(x, y, 40, 40)
            self.mask = pygame.mask.from_surface(self.image)

        def update(self):
            if self.fading and self.image.get_alpha():
                self.image.set_alpha(self.image.get_alpha() - 8)
                if self.image.get_alpha() == 0:
                    self.kill()
            else:
                self.image.fill((0, 0, 0))
                pygame.draw.circle(self.image, self.color, (20, 20), 14)
                pygame.draw.circle(self.image, (0, 0, 0), (20, 20), 16, 2)
        ##                print(get_rotation(mouse_pos, get_angle(pl.rect.x, pl.rect.y, mouse_pos[0], mouse_pos[1])))
                results = rotatePivoted(self.gun, 180 - degrees(atan2(pl.rect.centery - self.rect.centery, pl.rect.centerx - self.rect.centerx)), (self.rect.width // 2, self.rect.height // 2))
        ##                print(-degrees(atan2(mouse_pos[1] - pl.rect.y + 19, mouse_pos[0] - pl.rect.x + 17)))
                self.image.blit(results[0], results[1])
                results = None
                if self.active:
                    if self.cooldown == 0:
                        self.rockets = self.max_rockets # 3
                        self.release_cooldown = 0
                        self.cooldown = self.const_cooldown # 240
                    else:
                        self.cooldown -= 1
                    if self.rockets:
                        if self.release_cooldown == 0:
            ##                print(self.rect.centery, self.rect.y + 20, self.rect.y - 20)
                            ratio = 4 / sqrt((pl.rect.centery - self.rect.centery) ** 2 + (pl.rect.centerx - self.rect.centerx) ** 2)
                            Projectile(enemy_projectiles, self.rect.centerx, self.rect.centery,
                                       -degrees(atan2(pl.rect.centery - self.rect.centery, pl.rect.centerx - self.rect.centerx)),
                                       (ratio * (pl.rect.centerx - self.rect.centerx), ratio * (pl.rect.centery - self.rect.centery)),
                                       self.color)
                            self.rockets -= 1
                            self.release_cooldown = self.fire_delay # 25
                        else:
                            self.release_cooldown -= 1
                    if pygame.sprite.collide_mask(pl, self):
                        gameover_screen(score)
                else:
                    if self.initial_cooldown == 0:
                        self.image.set_alpha(255)
                        self.active = True
                    else:
                        self.initial_cooldown -= 1


    class Blinker(pygame.sprite.Sprite):
        def __init__(self, group, x, y, initial_cooldown, blink_delay, waiting_time, color):
            super().__init__(group)
            self.active = False
            self.vulnerable = False
            self.fading = False
    ##        self.point = pl.rect.center
            self.color = color
            self.invcolor = (255 - color.r, 255 - color.g, 255 - color.b)
            self.initial_cooldown = initial_cooldown
            self.blink_delay = blink_delay
            self.blink_cooldown = blink_delay
            self.const_cooldown = waiting_time
            self.cooldown = waiting_time
            self.tpoint = None
            self.image = pygame.Surface((40, 40))
            self.image.set_colorkey((0, 0, 0))
            pygame.draw.circle(self.image, self.color, (20, 20), 20, 3)
    ##        pygame.draw.circle(self.image, (255, 255, 255), (20, 20), 20, 1)
            self.arrow = pygame.Surface((50, 16))
            self.arrow.set_colorkey((0, 0, 0))
            pygame.draw.polygon(self.arrow, color, ((7, 8), (38, 0), (30, 8), (38, 16)))
    ##        pygame.draw.polygon(self.gun, (0, 0, 0), ((7, 8), (35, 0), (30, 8), (35, 16)), 1)
            self.image.blit(self.arrow, (0, 16))
            self.image.set_alpha(127)
            self.rect = pygame.Rect(x, y, 40, 40)
            self.mask = pygame.mask.from_surface(self.image)

        def generate_target_point(self):
            ratio = 4 / sqrt((pl.rect.centery - self.rect.y) ** 2 + (pl.rect.centerx - self.rect.x) ** 2)
            output = [round(self.rect.x + (ratio * (pl.rect.centerx + random.randint(-100, 100) - self.rect.x)) * 50), \
                     round(self.rect.y + (ratio * (pl.rect.centery + random.randint(-100, 100) - self.rect.y)) * 50)]
            if output[0] < 0:
                output[0] = 0
            elif output[0] + self.rect.width > width:
                 output[0] = width - self.rect.width
            if output[1] < ceiling.rect.bottom:
                output[1] = ceiling.rect.bottom
            elif output[1] + self.rect.height > floor.rect.top:
                output[1] = floor.rect.top - self.rect.height
            return output
        
        def point_at(self, pos):
            self.image.fill((0, 0, 0))
            pygame.draw.circle(self.image, self.color, (20, 20), 20, 4)
            results = rotatePivoted(self.arrow, 180 - degrees(atan2(pos[1] - self.rect.y, pos[0] - self.rect.x)), (self.rect.width // 2, self.rect.height // 2))
            self.image.blit(results[0], results[1])
            
        def update(self):
            if self.fading and self.image.get_alpha():
                self.image.set_alpha(self.image.get_alpha() - 8)
                if self.image.get_alpha() == 0:
                    self.kill()
            else:
                if self.active:
                    if self.cooldown != 0:
                        if not self.vulnerable and self.cooldown < self.const_cooldown // 2:
                            self.vulnerable = True
                        self.arrow.fill((0, 0, 0))
                        pygame.draw.polygon(self.arrow, self.color, ((7, 8), (38, 0), (30, 8), (38, 16)))
                        self.point_at(pl.rect.center)
                        self.cooldown -= 1
                    elif self.tpoint is None:
                        self.tpoint = self.generate_target_point()
                        self.arrow.fill((0, 0, 0))
                        pygame.draw.polygon(self.arrow, self.invcolor, ((7, 8), (38, 0), (30, 8), (38, 16)))
                        self.point_at(self.tpoint)
                    elif self.blink_cooldown != 0:
                        self.blink_cooldown -= 1
                    else:
                        if self.tpoint != (self.rect.x, self.rect.y):
                            Laser(enemy_explosions, self.rect.center, (self.tpoint[0] + self.rect.width // 2, self.tpoint[1] + self.rect.height // 2), self.color, 12)
                            self.rect.x, self.rect.y = self.tpoint
                        self.tpoint = None
                        self.blink_cooldown = self.blink_delay
                        self.cooldown = self.const_cooldown
                        self.vulnerable = False
                    if pygame.sprite.collide_mask(pl, self):
                        gameover_screen(score)
                else:
                    self.point_at(pl.rect.center)
                    if self.initial_cooldown == 0:
                        self.image.set_alpha(255)
                        self.active = True
                    else:
                        self.initial_cooldown -= 1

        
    class Enemy_explosion(pygame.sprite.Sprite):
        def __init__(self, group, x, y, color, radius, loops):
            super().__init__(group)
            self.max_radius = radius + 5
            self.radius = 2
            self.color = color
            self.loops = loops
            self.image = pygame.Surface((self.max_radius * 2, self.max_radius * 2))
            self.image.set_colorkey((0, 0, 0))
            self.rect = pygame.Rect(x - radius, y - radius, self.max_radius * 2,  self.max_radius * 2)
            self.mask = pygame.mask.from_surface(self.image)
            
        def update(self):
            self.image.fill((0, 0, 0))
            pygame.draw.circle(self.image, self.color, (self.rect.width // 2, self.rect.height // 2), self.radius, 2)
            self.radius += 1
            if self.radius == self.max_radius:
                self.radius = 2
                self.loops -= 1
                if self.loops == 0:
                    self.kill()
            if pygame.sprite.collide_circle(self, pl):
                gameover_screen(score)


    class Laser(pygame.sprite.Sprite):
        def __init__(self, group, pos1, pos2, color, thickness):
            super().__init__(group)
            self.max_width = thickness
            self.width = 1
            self.color = color
            self.shrinking = False
            self.image = pygame.Surface((abs(pos1[0] - pos2[0]) + self.max_width, abs(pos1[1] - pos2[1]) + self.max_width))
            self.image.set_colorkey((0, 0, 0))
    ##        self.rect = pygame.Rect(min(pos1[0], pos2[0]) - self.max_width, min(pos1[1], pos2[1]) - self.max_width, abs(pos1[0] - pos2[0]) - self.max_width ,  abs(pos1[1] - pos2[1]) - self.max_width)
            self.rect = pygame.Rect(min(pos1[0], pos2[0]) - self.max_width // 2, min(pos1[1], pos2[1]) - self.max_width // 2, abs(pos1[0] - pos2[0]) + self.max_width,  abs(pos1[1] - pos2[1]) + self.max_width)
            self.pos1 = (pos1[0] - self.rect.x, pos1[1] - self.rect.y)
            self.pos2 = (pos2[0] - self.rect.x, pos2[1] - self.rect.y)
    ##        print(pos1, self.pos1, pos2, self.pos2)
            
            
        def update(self):
            self.image.fill((0, 0, 0))
            pygame.draw.line(self.image, self.color, self.pos1, self.pos2, self.width)
            self.mask = pygame.mask.from_surface(self.image)
    ##        pygame.draw.circle(self.image, self.color, (self.rect.width // 2, self.rect.height // 2), self.radius, 2)
            if not self.shrinking:
                self.width += 1
            else:
                self.width -= 1
            if self.width == self.max_width:
                self.shrinking = True
            if self.width == 0:
                self.kill()
            if pygame.sprite.collide_mask(self, pl):
                gameover_screen(score)
                
    running = True
    


    Ground(background, (width, int(150 / 700 * height)), (50, 50, 50), 0, height - int(150 / 700 *
                                                                                       height))
    Ground(background, (width, int(150 / 700 * height)), (50, 50, 50), 0, 0)


    floor = Ground(ground, (width, int(110 / 700 * height)), (80, 80, 80), 0, height - int(110 /
                                                                                           700 * height))
    ceiling = Ground(ground, (width, int(110 / 700 * height)), (80, 80, 80), 0, 0)

    mouse_pos = (width, floor.rect.top - 18)
    space = False
    speed = 1
    game_started = False
    fullscreen = False
    pause = False

    pl = Player(players, (width + 34) // 2, floor.rect.top - 36)

    lastbbs = None # last back bottom stalactite
    lastbts = None # last back top stalactite
    lastfs = None # last front stalactite

    # cooldowns until something can spawn

    bbscd = 0
    btscd = 0
    fscd = 360

    platform_cooldown = 360
    enemy_cooldown = 360
    score = 0
    
    ##Stalactite(decorations, width, 200, 40, 50, (50, 50, 50), 1, False)
    global screen
    try:
        while running:
            screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
                if event.type == pygame.MOUSEMOTION:
                    mouse_pos = event.pos
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and pl.cooldown == 0:
                        ratio = 4 / sqrt((event.pos[1] - pl.rect.y - 19) ** 2 + (event.pos[0] - pl.rect.x - 17) ** 2)
                        Projectile(projectiles, pl.rect.x + 17, pl.rect.y + 19,
                                   -degrees(atan2(event.pos[1] - pl.rect.y - 19, event.pos[0] - pl.rect.x - 17)),
                                   (ratio * (event.pos[0] - pl.rect.x - 17), ratio * (event.pos[1] - pl.rect.y - 19)),
                                   pygame.Color('red'))
                        game_started = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        pl.direction = -3
                    elif event.key == pygame.K_d:
                        pl.direction = 3
                    elif event.key == pygame.K_SPACE:
                        space = True
                    elif event.key == pygame.K_F1:
                        if fullscreen:
                            pause = True
                            screen = pygame.display.set_mode(size)
                            fullscreen = False
                        else:
                            pause = True
                            screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
                            fullscreen = True
                    elif event.key == pygame.K_p:
                        pause = True
                elif event.type == pygame.KEYUP:
                    if pl.direction < 0 and event.key == pygame.K_a:
                        pl.direction = 0
                    elif pl.direction > 0 and event.key == pygame.K_d:
                        pl.direction = 0
                    elif event.key == pygame.K_w:
                        pl.yvel = 0
                    elif event.key == pygame.K_s:
                        pl.yvel = 0
                    elif event.key == pygame.K_SPACE:
                        space = False

            if pause:
##                text_controller = [True, 80]
                pause_text = pygame.font.Font(None, 100).render('Пауза', 1, (0, 0, 0), (255, 255, 255))
                while True:
                    for e in pygame.event.get():
                        if e.type == pygame.QUIT:
                            pygame.quit()
                            raise SystemExit
                        elif e.type == pygame.MOUSEMOTION:
                            mouse_pos = e.pos
                        elif e.type == pygame.KEYDOWN:
                            if e.key == pygame.K_a:
                                pl.direction = -3
                            elif e.key == pygame.K_d:
                                pl.direction = 3
                            elif e.key == pygame.K_SPACE:
                                space = True
                            elif e.key == pygame.K_F1:
                                if fullscreen:
                                    screen = pygame.display.set_mode(size)
                                    fullscreen = False
                                else:
                                    screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
                                    fullscreen = True
                            elif e.key == pygame.K_p:
                                break
                        elif e.type == pygame.KEYUP:
                            if pl.direction < 0 and e.key == pygame.K_a:
                                pl.direction = 0
                            elif pl.direction > 0 and e.key == pygame.K_d:
                                pl.direction = 0
                            elif e.key == pygame.K_w:
                                pl.yvel = 0
                            elif e.key == pygame.K_s:
                                pl.yvel = 0
                            elif e.key == pygame.K_SPACE:
                                space = False
                    else:
                        screen.fill((0, 0, 0))
                        background.draw(screen)
                        decorations.draw(screen)
                        ground.draw(screen)
                        platforms.draw(screen)   
                        explosions.draw(screen)
                        enemy_explosions.draw(screen)
                        enemy_projectiles.draw(screen)
                        projectiles.draw(screen)
                        ranged_enemies.draw(screen)
                        melee_enemies.draw(screen)
                        players.draw(screen)
                        foreground.draw(screen)
                        screen.blit(score_label, ((width - score_label.get_rect().width) // 2, 30))
##                        if text_controller[1] == 0:
##                            text_controller[0] = not text_controller[0]
##                            text_controller[1] = 80
##                        else:
##                            text_controller[1] -= 1
##                        if text_controller[0]:
                        screen.blit(pause_text, ((width - pause_text.get_rect().width) // 2, (height - pause_text.get_rect().height) // 2))
                        pygame.display.flip()
                        clock.tick(fps)
                        continue
                    pause = False
                    break

            if game_started:
                
                score += 1
                if score // 120 == 120:
                    speed = 2
                if btscd == 0:
                    if rng(50):
                        if lastbts is not None and lastbts.rect.x + lastbts.length < width + 10:
                            stwidth = random.randint(35, width - lastbts.rect.x + lastbts.length) \
                                      if width - lastbts.rect.x < 80 \
                                      else random.randint(35, 80)
                            lastbts = Stalactite(decorations,
                                                 width + 16,
                                                 int(150 / 700 * height),
                                                 stwidth,
                                                 (50, 50, 50),
                                                 0.5,
                                                 False)
                        elif lastbts is None:
                            lastbts = Stalactite(decorations,
                                                 width,
                                                 int(150 / 700 * height),
                                                 random.randint(15, 45),
                                                 (50, 50, 50),
                                                 0.5,
                                                 False)
                    btscd = 60
                else:
                    btscd -= 1

                if bbscd == 0:
                    if rng(50):
                        if lastbbs is not None and lastbbs.rect.x + lastbbs.length < width + 10:
                            stwidth = random.randint(35, width - lastbbs.rect.x + lastbbs.length) \
                                      if width - lastbbs.rect.x < 80 \
                                      else random.randint(35, 80)
                            lastbbs = Stalactite(decorations,
                                                 width + 16,
                                                 height - int(150 / 700 * height),
                                                 stwidth,
                                                 (50, 50, 50),
                                                 0.5,
                                                 True)
                        elif lastbbs is None:
                            lastbbs = Stalactite(decorations,
                                                 width,
                                                 height - int(150 / 700 * height),
                                                 random.randint(15, 45),
                                                 (50, 50, 50),
                                                 0.5,
                                                 True)
                    bbscd = 60
                else:
                    bbscd -= 1
                    
                if lastfs not in foreground:
                    if fscd == 0:
                        if rng(10):
                            if random.randint(0, 1):
                                lastfs = Stalactite(foreground,
                                                    width + 16,
                                                    0,
                                                    random.randint(200, 400),
                                                    (1, 1, 1),
                                                    2,
                                                    False,
                                                    (40, 40, 40))
                            else:
                                lastfs = Stalactite(foreground,
                                                    width + 16,
                                                    height,
                                                    random.randint(200, 400),
                                                    (1, 1, 1),
                                                    2,
                                                    True,
                                                    (40, 40, 40))
                        fscd = 60
                    else:
                        fscd -= 1

                if platform_cooldown == 0:
                    if rng(75):
                        Ground(platforms, (125, 15), (80, 80, 80), width, random.randint(ceiling.rect.bottom + 125, floor.rect.top - 125))
                    platform_cooldown = 360
                else:
                    platform_cooldown -= 1

                if enemy_cooldown == 0:
                    if rng(80):
                        if random.randint(0, 1):
                            if rng(85):
                                Gunner(ranged_enemies, random.randint(0, width - 40), random.randint(ceiling.rect.bottom, floor.rect.top - 40), 100, 300, 25, 3, pygame.Color('green'))
                            else:
                                Gunner(ranged_enemies, random.randint(0, width - 40), random.randint(ceiling.rect.bottom, floor.rect.top - 40), 100, 240, 15, 6, pygame.Color('purple'))
                        else:
                            if rng(85):
                                Blinker(melee_enemies, random.randint(0, width - 40), random.randint(ceiling.rect.bottom, floor.rect.top - 40), 100, 75, 75, pygame.Color('green'))
                            else:
                                Blinker(melee_enemies, random.randint(0, width - 40), random.randint(ceiling.rect.bottom, floor.rect.top - 40), 100, 50, 50, pygame.Color('purple'))
                        
                    enemy_cooldown = 240
                else:
                    enemy_cooldown -= 1
                    
            if pl.cooldown != 0:
                pl.cooldown -= 1
            if mouse_pos is not None:
    ##                angle = degrees(atan2(mouse_pos[1], mouse_pos[0]))
    ##                print(angle)
                pl.image.fill((0, 0, 0))
                pygame.draw.rect(pl.image, pygame.Color("blue"),
                     (7, 0, 20, 36))
    ##                print(get_rotation(mouse_pos, get_angle(pl.rect.x, pl.rect.y, mouse_pos[0], mouse_pos[1])))
                results = rotatePivoted(
                    pl.gun, -degrees(atan2(mouse_pos[1] - pl.rect.y - 19, mouse_pos[0] - pl.rect.x - 17)), (17, 19))
    ##                print(-degrees(atan2(mouse_pos[1] - pl.rect.y + 19, mouse_pos[0] - pl.rect.x + 17)))
                pl.image.blit(results[0], results[1])
                results = None
            
            if space and pl.on_ground:
                pl.on_ground = False
                pl.yvel = -8

    ##            if pl.on_ground and pl.yvel >= 0:
                
    ##                    pl.yvel = 0

            else:
                pl.move(0, pl.yvel)
                for pf in platforms:
                    if pygame.sprite.collide_mask(pl, pf) and pf.below_player and pl.yvel >= 0:
                        pl.on_ground = True
                        pl.move(0, pf.rect.top - pl.rect.bottom)
                        break
                else:
                    if pygame.sprite.collide_mask(pl, ceiling):
                        pl.move(0, ceiling.rect.bottom - pl.rect.top)
                        pl.yvel = 0
                        
                    elif pygame.sprite.collide_mask(pl, floor):
                        pl.on_ground = True
                        pl.move(0, floor.rect.top - pl.rect.bottom)
                        
                    else:
                        pl.on_ground = False
    ##                        pl.move(0, pl.yvel)

            if pl.on_ground and game_started:
                pl.move(-speed, 0)
            pl.move(pl.xvel + pl.direction, 0)
            
            if pl.rect.x < -8:
                pl.rect.x = -8
                pl.xvel = 0

            elif pl.rect.x + 27 > width:
                pl.rect.x = width - 27
                pl.xvel = 0

            if not pl.on_ground:
                if pl.yvel + 0.3 <= 8:
                    pl.yvel += 0.3
                else:
                    pl.yvel = 8
            else:
                pl.yvel = 1
                
            if pl.xvel >= 0.1:
                pl.xvel -= 0.1
            elif pl.xvel <= -0.1:
                pl.xvel += 0.1
            else:
                pl.xvel = 0

            if score % 120 == 0:
                score_label = pygame.font.Font(None, 75).render(str(score // 120), 1, (175, 175, 175))

            background.draw(screen)
            decorations.draw(screen)
            decorations.update()
            ground.draw(screen)
            platforms.draw(screen)
            platforms.update()      
            explosions.draw(screen)
            explosions.update()
            enemy_explosions.draw(screen)
            enemy_explosions.update()
            enemy_projectiles.draw(screen)
            enemy_projectiles.update()
            projectiles.draw(screen)
            projectiles.update()
            ranged_enemies.draw(screen)
            ranged_enemies.update()
            melee_enemies.draw(screen)
            melee_enemies.update()
            players.draw(screen)
            foreground.draw(screen)
            foreground.update()
            screen.blit(score_label, ((width - score_label.get_rect().width) // 2, 30))
            pygame.display.flip()
            clock.tick(fps)

    finally:
        pygame.quit()


clock = pygame.time.Clock()
start_screen()
start()

