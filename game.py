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
projectiles = pygame.sprite.Group()
explosions = pygame.sprite.Group()
decorations = pygame.sprite.Group()


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
        pygame.draw.circle(self.image, (255, 255, 0), (radius, radius), int(radius / 1.5))
        self.rect = pygame.Rect(x, y, radius * 2,  radius * 2)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        if self.stage == 5:
            pygame.draw.circle(self.image, (255, 165, 0), (self.radius, self.radius), int(self.radius // 3 * 2), int(self.radius // 3))
            self.stage += 1
        elif self.stage == 10:
            pygame.draw.circle(self.image, (255, 0, 0), (self.radius, self.radius), int(self.radius), int(self.radius // 3))
            self.stage += 1
        elif self.stage == 15:
            self.image.fill((0, 0, 0))
            pygame.draw.circle(self.image, (255, 255, 0), (self.radius, self.radius), int(self.radius // 3))
            pygame.draw.circle(self.image, (255, 165, 0), (self.radius, self.radius), int(self.radius // 3 * 2), int(self.radius // 3))
            self.stage += 1
        elif self.stage == 20:
            self.image.fill((0, 0, 0))
            pygame.draw.circle(self.image, (255, 255, 0), (self.radius, self.radius), int(self.radius // 3))
            self.stage += 1
        elif self.stage == 25:
            self.kill()
        else:
            self.stage += 1

            
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
    def __init__(self, group, x, y, rotation, velocity, friendly):
        super().__init__(group)
        self.xremainder = 0
        self.yremainder = 0
        self.image = pygame.Surface((14, 8))
        self.image.set_colorkey((0, 0, 0))
        pygame.draw.polygon(self.image, pygame.Color('red'), ((0, 0), (14, 4), (0, 8)))
        pygame.draw.polygon(self.image, (0, 0, 0), ((0, 0), (14, 4), (0, 8)), 1)
        self.image = pygame.transform.rotate(self.image, rotation)
        self.rect = pygame.Rect(x, y, 14, 8)
        self.mask = pygame.mask.from_surface(self.image)
        self.velx = velocity[0] * 2.5
        self.vely = velocity[1] * 2.5
        if friendly:
            pl.cooldown = 35
            pl.xvel -= velocity[0] * 1.5
            pl.yvel -= velocity[1] * 1.5
            if pl.yvel <= 0 and pl.on_ground:
                pl.on_ground = False
        
    def move(self):
        self.rect = self.rect.move(self.velx + self.xremainder, self.vely + self.yremainder)
        self.xremainder = self.velx + self.xremainder - int(self.velx + self.xremainder)
        self.yremainder = self.vely + self.yremainder - int(self.vely + self.yremainder)

    def explode(self):
        self.kill()
        Explosion(explosions, self.rect.x - 30, self.rect.y - 30, 30)


class Ground(pygame.sprite.Sprite):
    def __init__(self, group, size, color, x, y):
        super().__init__(group)
        self.image = pygame.Surface(size,
                                    pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, color,
                           (0, 0, size[0], size[1]))
        self.rect = pygame.Rect(x, y, size[0], size[1])
        self.mask = pygame.mask.from_surface(self.image)

class Stalactite(pygame.sprite.Sprite):
    def __init__(self, group, x, y, length, color, multiplier, upside_down):
        super().__init__(group)
        self.length = length
        self.cooldown = 0
        if multiplier < 1:
            self.multiplier = 1
            self.max_cooldown = 1 // multiplier
        else:
            self.multiplier = multiplier
            self.max_cooldown = 0
        self.height = random.randint(length // 2, length)
        self.image = pygame.Surface((length, height))
        self.image.set_colorkey((0, 0, 0))
        if not upside_down:
            pygame.draw.polygon(self.image, color, ((0, 0), (length // 2, self.height), (length, 0)))
        else:
            pygame.draw.polygon(self.image, color, ((0, self.height), (length // 2, 0), (length, self.height)))
##        pygame.draw.rect(self.image, color,
##                           (0, 0, size[0], size[1]))
        self.rect = pygame.Rect(x, y, length, self.height)
        self.mask = pygame.mask.from_surface(self.image)
        
    def move(self, xvelocity):
        self.rect = self.rect.move(xvelocity, 0)
        
    def update(self):
        if self.cooldown == 0:
            self.move(-speed * self.multiplier)
            if self.rect.x + self.length < 0:
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


Ground(background, (900, 200), (50, 50, 50), 0, 500)
Ground(background, (900, 200), (50, 50, 50), 0, 0)


floor = Ground(ground, (900, 150), (80, 80, 80), 0, 550)
ceiling = Ground(ground, (900, 150), (80, 80, 80), 0, 0)

lastfbs = None # last front bottom stalactite
lastbbs = None # last back bottom stalactite
lastfts = None # last front top stalactite
lastbts = None # last back top stalactite

# cooldowns until a new stalactite can be created
fbscd = 0
bbscd = 0
ftscd = 0
btscd = 0

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
                               (ratio * (event.pos[0] - pl.rect.x - 17), ratio * (event.pos[1] - pl.rect.y - 19)), True)
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
            if lastbts is not None and width - lastbts.rect.x > 15 and rng(3):
                stwidth = random.randint(15, width - lastbts.rect.x) \
                          if width - lastbts.rect.x < 80 \
                          else random.randint(15, 80)
                lastbts = Stalactite(decorations,
                                     width - stwidth + 16,
                                     200,
                                     stwidth,
                                     (50, 50, 50),
                                     0.5,
                                     False)
            elif lastbts is None and rng(6):
                lastbts = Stalactite(decorations,
                                     width,
                                     200,
                                     random.randint(15, 45),
                                     (50, 50, 50),
                                     0.5,
                                     False)
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
                pl.yvel = -4

##            if pl.on_ground and pl.yvel >= 0:
                
##                    pl.yvel = 0

            else:
                pl.move(0, pl.yvel)
                if pygame.sprite.collide_mask(pl, ceiling):
                    pl.move(0, 155 - pl.rect.y)
                    pl.yvel = 0
                    
                elif pygame.sprite.collide_mask(pl, floor):
                    pl.on_ground = True
                    pl.move(0, 550 - 36 - pl.rect.y)
                    
                else:
                    pl.move(0, pl.yvel)

            if pl.on_ground:
                pl.move(-speed, 0)
            pl.move(pl.xvel + pl.direction, 0)
            
            if pl.rect.x < -8:
                pl.rect.x = -8

            elif pl.rect.x + 27 > width:
                pl.rect.x = width - 27
                
            if pl.yvel + 0.15 <= 4:
                pl.yvel += 0.15
            else:
                pl.yvel = 4
                
            if pl.xvel >= 0.1:
                pl.xvel -= 0.1
            elif pl.xvel <= -0.1:
                pl.xvel += 0.1
            else:
                pl.xvel = 0
##            print(pl.direction, pl.xvel, pl.yvel)
##        for sprite in players:
##            sprite.update()
        background.draw(screen)
        decorations.draw(screen)
        decorations.update()
        ground.draw(screen)
        enemies.draw(screen)
        for projectile in projectiles:
            projectile.move()
            if pygame.sprite.spritecollideany(projectile, ground):
                projectile.explode()
                
            if projectile.rect.x < -10:
                projectile.kill()

            if projectile.rect.x > width + 10:
                projectile.kill()
                
        explosions.draw(screen)
        explosions.update()
        projectiles.draw(screen)
        players.draw(screen)
        pygame.display.flip()
        clock.tick(fps)
        
finally:
    pygame.quit()

