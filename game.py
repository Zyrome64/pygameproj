import pygame
import random
from math import sqrt

pygame.init()
size = width, height = 900, 700
fps = 120
screen = pygame.display.set_mode(size)
players = pygame.sprite.Group()
enemies = pygame.sprite.Group()
background = pygame.sprite.Group()
ground = pygame.sprite.Group()

tgtable = {0: 0.0, 1: 0.0175, 2: 0.0349, 3: 0.0524, 4: 0.0699, 5: 0.0875, 6: 0.1051,
           7: 0.1228, 8: 0.1405, 9: 0.1584, 10: 0.1763, 11: 0.1944, 12: 0.2126,
           13: 0.2309, 14: 0.2493, 15: 0.2679, 16: 0.2867, 17: 0.3057, 18: 0.3249,
           19: 0.3443, 20: 0.364, 21: 0.3839, 22: 0.404, 23: 0.4245, 24: 0.4452,
           25: 0.4663, 26: 0.4877, 27: 0.5095, 28: 0.5317, 29: 0.5543, 30: 0.5774,
           31: 0.6009, 32: 0.6249, 33: 0.6494, 34: 0.6745, 35: 0.7002, 36: 0.7265,
           37: 0.7536, 38: 0.7813, 39: 0.8098, 40: 0.8391, 41: 0.8693, 42: 0.9004,
           43: 0.9325, 44: 0.9657, 45: 1.0, 46: 1.0355, 47: 1.0724, 48: 1.1106,
           49: 1.1504, 50: 1.1918, 51: 1.2349, 52: 1.2799, 53: 1.327, 54: 1.3764,
           55: 1.4281, 56: 1.4826, 57: 1.5399, 58: 1.6003, 59: 1.6643, 60: 1.7321,
           61: 1.804, 62: 1.8807, 63: 1.9626, 64: 2.0503, 65: 2.1445, 66: 2.246,
           67: 2.3559, 68: 2.4751, 69: 2.6051, 70: 2.7475, 71: 2.9042, 72: 3.0777,
           73: 3.2709, 74: 3.4874, 75: 3.7321, 76: 4.0108, 77: 4.3315, 78: 4.7046,
           79: 5.1446, 80: 5.6713, 81: 6.3138, 82: 7.1154, 83: 8.1443, 84: 9.5144,
           85: 11.4301, 86: 14.3007, 87: 19.0811, 88: 28.6363, 89: 57.29}

decorations = pygame.sprite.Group()


def rotatePivoted(im, angle, pivot):
    image = pygame.transform.rotate(im, angle)
    rect = image.get_rect()
    rect.center = pivot
    return image, rect


def get_angle(x1, y1, x2, y2):
    try:
        tg = abs(abs(y1) - abs(y2)) / abs(abs(x1) - abs(x2))
    except ZeroDivisionError:
        return 90
    if tg > 60:
        return 90 
    closest_angle = 0
    for i in range(1, 90):
        if abs(tgtable[closest_angle] - tg) > abs(tgtable[i] - tg):
            closest_angle = i
    return closest_angle


def get_rotation(pos, angle):
    angle = abs(angle % 90)
##    print(angle, '!')
    if pos[1] <= pl.rect.y + 19:
        if pos[0] >= pl.rect.x + 17:
            return angle
        else:
            return 180 - angle
    else:
        if pos[0] >= pl.rect.x + 17:
            return -angle
        else:
            return 180 + angle


class Player(pygame.sprite.Sprite):
    def __init__(self, group, x, y):
        super().__init__(group)
        self.on_ground = False
        self.image = pygame.Surface((36, 36),
                                    pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, pygame.Color("blue"),
                         (7, 0, 20, 36))
        self.gun = pygame.Surface((28, 8),
                                  pygame.SRCALPHA, 32)
        pygame.draw.rect(self.gun, pygame.Color('red'),
                         (8, 0, 20, 8))
        self.image.blit(self.gun, (14, 15))
        self.rect = pygame.Rect(x, y, 20,  36)
        self.mask = pygame.mask.from_surface(self.image)
        
    def move(self, xvelocity, yvelocity):
        self.rect = self.rect.move(xvelocity, yvelocity)


class Projectile(pygame.sprite.Sprite):
    def __init__(self, group, x, y):
        super().__init__(group)
##        self.on_ground = False
##        self.image = pygame.Surface((36, 36),
##                                    pygame.SRCALPHA, 32)
##        pygame.draw.rect(self.image, pygame.Color("blue"),
##                         (7, 0, 20, 36))
##        self.gun = pygame.Surface((28, 8),
##                                  pygame.SRCALPHA, 32)
##        pygame.draw.rect(self.gun, pygame.Color('red'),
##                         (8, 0, 20, 8))
##        self.image.blit(self.gun, (14, 15))
##        self.rect = pygame.Rect(x, y, 20,  36)
##        self.mask = pygame.mask.from_surface(self.image)
        
    def move(self, xvelocity, yvelocity):
        self.rect = self.rect.move(xvelocity, yvelocity)


class Missile(Projectile):
    pass


class Ground(pygame.sprite.Sprite):
    def __init__(self, group, size, color, x, y):
        super().__init__(group)
        self.image = pygame.Surface(size,
                                    pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, color,
                           (0, 0, size[0], size[1]))
        self.rect = pygame.Rect(x, y, size[0], size[1])
        self.mask = pygame.mask.from_surface(self.image)
        
        
running = True
clock = pygame.time.Clock()
pl = None
mouse_pos = None
mouse_angle = None
cur_pl_xvel = 0
cur_pl_yvel = 0
ctrl = False
space = False

Ground(background, (900, 200), (50, 50, 50), 0, 500)
Ground(background, (900, 200), (50, 50, 50), 0, 0)


floor = Ground(ground, (900, 150), (80, 80, 80), 0, 550)
ceiling = Ground(ground, (900, 150), (80, 80, 80), 0, 0)

try:
    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEMOTION:
                mouse_pos = event.pos
                if pl is not None:
                    mouse_angle = get_angle(pl.rect.x, pl.rect.y, mouse_pos[0], mouse_pos[1])
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not ctrl:
                    platform(ground, event.pos[0] - 100, event.pos[1] - 5)
##                elif event.button == 1 and ctrl:
##                    print(get_angle(pl.rect.x, pl.rect.y, event.pos[0], event.pos[1]))
##                    print(round(tg, 4), tg in tgtable.keys(), round(tg, 4) in tgtable.keys())
                elif event.button == 3:
                    if pl is not None:
                        players.remove(pl)
                    pl = Player(players, event.pos[0] - 15, event.pos[1] - 15)
            elif event.type == pygame.KEYDOWN:
                if pl is not None and event.key == pygame.K_a:
                    cur_pl_xvel = -3
                elif pl is not None and event.key == pygame.K_d:
                    cur_pl_xvel = 3
                elif pl is not None and pygame.sprite.spritecollideany(pl, enemies) and event.key == pygame.K_w:
                    cur_pl_yvel = -2
                elif pl is not None and pygame.sprite.spritecollideany(pl, enemies) and event.key == pygame.K_s:
                    cur_pl_yvel = 2 
                elif event.key == pygame.K_LCTRL:
                    ctrl = True
                elif event.key == pygame.K_SPACE:
                    space = True                        
            elif event.type == pygame.KEYUP:
                if pl is not None and cur_pl_xvel < 0 and event.key == pygame.K_a:
                    cur_pl_xvel = 0
                elif pl is not None and cur_pl_xvel > 0 and event.key == pygame.K_d:
                    cur_pl_xvel = 0
                elif event.key == pygame.K_w:
                    cur_pl_yvel = 0
                elif event.key == pygame.K_s:
                    cur_pl_yvel = 0
                elif event.key == pygame.K_SPACE:
                    space = False
                elif event.key == pygame.K_LCTRL:
                    ctrl = False

                    
        if pl is not None:
            if mouse_pos is not None and mouse_angle is not None:
                pl.image.convert_alpha()
                pygame.draw.rect(pl.image, pygame.Color("blue"),
                     (7, 0, 20, 36))
##                print(get_rotation(mouse_pos, get_angle(pl.rect.x, pl.rect.y, mouse_pos[0], mouse_pos[1])))
                results = rotatePivoted(
                    pl.gun, get_rotation(mouse_pos, mouse_angle), (17, 19))
                pl.image.blit(results[0], results[1])
                results = None
            
            if space and pl.on_ground:
                pl.on_ground = False
                cur_pl_yvel = -4

            if pl.on_ground and cur_pl_yvel >= 0:
                pl.move(cur_pl_xvel, 0)
                
            else:
                pl.move(0, cur_pl_yvel)
                if pygame.sprite.collide_mask(pl, ceiling):
                    pl.move(0, 155 - pl.rect.y)
                    cur_pl_y_vel = 1
                    
                elif pygame.sprite.collide_mask(pl, floor):
                    pl.on_ground = True
                    pl.move(0, 550 - 36 - pl.rect.y)
                    
                else:
                    pl.move(cur_pl_xvel, round(cur_pl_yvel))
            if cur_pl_yvel + 0.1 <= 4:
                cur_pl_yvel += 0.1
            else:
                cur_pl_yvel = 4
##        for sprite in players:
##            sprite.update()
        background.draw(screen)
        ground.draw(screen)
        enemies.draw(screen)
        players.draw(screen)
        pygame.display.flip()
        clock.tick(fps)
        
finally:
    pygame.quit()
