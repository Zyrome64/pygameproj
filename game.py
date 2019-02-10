import pygame
import random
from math import sqrt, atan2, degrees

pygame.init()
size = width, height = 900, 700
fps = 120
screen = pygame.display.set_mode(size)
players = pygame.sprite.Group()
enemies = pygame.sprite.Group()
background = pygame.sprite.Group()
ground = pygame.sprite.Group()
platforms = pygame.sprite.Group()
projectiles = pygame.sprite.Group()
enemy_projectiles = pygame.sprite.Group()
explosions = pygame.sprite.Group()
enemy_explosions = pygame.sprite.Group()
decorations = pygame.sprite.Group()
foreground = pygame.sprite.Group()


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
        for enemy in enemies:
            if pygame.sprite.collide_circle(self, enemy):
                enemy.kill()


class Enemy_explosion(pygame.sprite.Sprite):
    def __init__(self, group, x, y, color, radius, blinks):
        super().__init__(group)
        self.max_radius = radius + 5
        self.radius = 2
        self.color = color
        self.blinks = blinks
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
            self.blinks -= 1
            if self.blinks == 0:
                self.kill()
##        self.mask = pygame.mask.from_surface(self.image)
####        print(self.mask.)
        if pygame.sprite.collide_circle(self, pl):
            pl.kill()
        
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


class Gunner(pygame.sprite.Sprite):
    def __init__(self, group, x, y, initial_cooldown, ccd, fire_delay, max_rockets, color):
        super().__init__(group)
        self.active = False
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
                pl.kill()
        else:
            if self.initial_cooldown == 0:
                self.image.set_alpha(255)
                self.active = True
            else:
                self.initial_cooldown -= 1
       

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
            pl.yvel -= velocity[1] * 1.8
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
            Enemy_explosion(explosions, self.rect.x, self.rect.y, self.color, 16, 3)
        self.kill()

    def update(self):
        self.move()
        if self.friendly:
            for enemy in enemies:
                if pygame.sprite.collide_mask(self, enemy):
                    self.explode()
                    break
            else:
                if pygame.sprite.spritecollideany(self, ground) or pygame.sprite.spritecollideany(self, platforms):
                    self.explode()
        else:
            if pygame.sprite.spritecollideany(self, ground) or pygame.sprite.spritecollideany(self, platforms) or pygame.sprite.collide_mask(self, pl):
                self.explode()
            
        if self.rect.x < -10:
            self.kill()

        if self.rect.x > width + 10:
            self.kill()


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

##        pygame.draw.rect(self.image, color,
##                           (0, 0, size[0], size[1]))
        
            
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

            
running = True
clock = pygame.time.Clock()
pl = None
mouse_pos = None
angle = None
ctrl = False
space = False
speed = 1


Ground(background, (900, 150), (50, 50, 50), 0, 550)
Ground(background, (900, 150), (50, 50, 50), 0, 0)


floor = Ground(ground, (900, 110), (80, 80, 80), 0, 590)
ceiling = Ground(ground, (900, 110), (80, 80, 80), 0, 0)

lastbbs = None # last back bottom stalactite
lastbts = None # last back top stalactite
lastfs = None # last front stalactite

# cooldowns until something can spawn

bbscd = 0
btscd = 0
fscd = 360

platform_cooldown = 360
enemy_cooldown = 360
##Stalactite(decorations, width, 200, 40, 50, (50, 50, 50), 1, False)
try:
    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEMOTION:
                mouse_pos = event.pos
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and pl is not None and pl.cooldown == 0:
                    ratio = 4 / sqrt((event.pos[1] - pl.rect.y - 19) ** 2 + (event.pos[0] - pl.rect.x - 17) ** 2)
                    Projectile(projectiles, pl.rect.x + 17, pl.rect.y + 19,
                               -degrees(atan2(event.pos[1] - pl.rect.y - 19, event.pos[0] - pl.rect.x - 17)),
                               (ratio * (event.pos[0] - pl.rect.x - 17), ratio * (event.pos[1] - pl.rect.y - 19)),
                               pygame.Color('red'))
##                elif event.button == 1 and ctrl:
##                    print(get_angle(pl.rect.x, pl.rect.y, event.pos[0], event.pos[1]))
##                    print(round(tg, 4), tg in tgtable.keys(), round(tg, 4) in tgtable.keys())
                if event.button == 3:
                    if pl is not None:
                        players.remove(pl)
                    pl = Player(players, event.pos[0] - 15, event.pos[1] - 15)
            elif event.type == pygame.KEYDOWN:
                if pl is not None and event.key == pygame.K_a:
                    pl.direction = -3
                elif pl is not None and event.key == pygame.K_d:
                    pl.direction = 3
##                elif pl is not None and pygame.sprite.spritecollideany(pl, enemies) and event.key == pygame.K_w:
##                    pl.yvel = -2
##                elif pl is not None and pygame.sprite.spritecollideany(pl, enemies) and event.key == pygame.K_s:
##                    pl.yvel = 2 
                elif event.key == pygame.K_LCTRL:
                    ctrl = True
                elif event.key == pygame.K_SPACE:
                    space = True                        
            elif event.type == pygame.KEYUP:
                if pl is not None and pl.direction < 0 and event.key == pygame.K_a:
                    pl.direction = 0
                elif pl is not None and pl.direction > 0 and event.key == pygame.K_d:
                    pl.direction = 0
                elif event.key == pygame.K_w:
                    pl.yvel = 0
                elif event.key == pygame.K_s:
                    pl.yvel = 0
                elif event.key == pygame.K_SPACE:
                    space = False
                elif event.key == pygame.K_LCTRL:
                    ctrl = False

                    
        if pl is not None:
            if btscd == 0:
                if rng(50):
                    if lastbts is not None and lastbts.rect.x + lastbts.length < width + 10:
                        stwidth = random.randint(35, width - lastbts.rect.x + lastbts.length) \
                                  if width - lastbts.rect.x < 80 \
                                  else random.randint(35, 80)
                        lastbts = Stalactite(decorations,
                                             width + 16,
                                             150,
                                             stwidth,
                                             (50, 50, 50),
                                             0.5,
                                             False)
                    elif lastbts is None:
                        lastbts = Stalactite(decorations,
                                             width,
                                             150,
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
                                             550,
                                             stwidth,
                                             (50, 50, 50),
                                             0.5,
                                             True)
                    elif lastbbs is None:
                        lastbbs = Stalactite(decorations,
                                             width,
                                             550,
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
                    if rng(85):
                        Gunner(enemies, random.randint(0, width - 40), random.randint(ceiling.rect.bottom, floor.rect.top - 40), 100, 240, 25, 3, pygame.Color('green'))
                    else:
                        Gunner(enemies, random.randint(0, width - 40), random.randint(ceiling.rect.bottom, floor.rect.top - 40), 100, 180, 20, 6, pygame.Color('purple'))
                enemy_cooldown = 240
            else:
                enemy_cooldown -= 1
                
            if pl.cooldown > 0:
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

            if pl.on_ground:
                pl.move(-speed, 0)
            pl.move(pl.xvel + pl.direction, 0)
            
            if pl.rect.x < -8:
                pl.rect.x = -8

            elif pl.rect.x + 27 > width:
                pl.rect.x = width - 27

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
##        for projectile in projectiles:
##            projectile.move()
##            if pygame.sprite.spritecollideany(projectile, ground) or pygame.sprite.spritecollideany(projectile, platforms) :
##                projectile.explode()
##                
##            if projectile.rect.x < -10:
##                projectile.kill()
##
##            if projectile.rect.x > width + 10:
##                projectile.kill()
####################
##        for projectile in enemy_projectiles:
##            projectile.move()
##            if pygame.sprite.spritecollideany(projectile, ground) or pygame.sprite.spritecollideany(projectile, platforms):
##                projectile.explode()
##                
##            if projectile.rect.x < -10:
##                projectile.kill()
##
##            if projectile.rect.x > width + 10:
##                projectile.kill()
##            print(pl.direction, pl.xvel, pl.yvel)
##        for sprite in players:
##            sprite.update()

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
        enemies.draw(screen)
        enemies.update()
        players.draw(screen)
        foreground.draw(screen)
        foreground.update()
        pygame.display.flip()
        clock.tick(fps)
        
finally:
    pygame.quit()

