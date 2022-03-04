from os import path
import pygame
import random

fps = 60
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
width, height = pygame.display.get_surface().get_size()
pygame.display.set_caption('My game')
clock = pygame.time.Clock()

img_dir = path.join(path.dirname(__file__), 'Images')
fon = pygame.image.load(path.join(img_dir, 'Космос.jpeg')).convert()
fon = pygame.transform.scale(fon, (width, height))
fon_rect = fon.get_rect()

fon_pula = pygame.image.load(path.join(img_dir, 'laserRed12.png')).convert()
fonmetr = []
for metr in range(1, 10 + 1):
    fon_meteor = pygame.image.load(path.join(img_dir, 'meteorGrey_big{}.png'.format(metr))).convert()
    fonmetr.append(fon_meteor)
fon_player = pygame.image.load(path.join(img_dir, 'playerShip2_blue.png')).convert()

Boom = []
for booms in range(0, 8 + 1):
    boomy = pygame.image.load(path.join(img_dir, 'regularExplosion0{}.png'.format(booms))).convert()
    boomy.set_colorkey((0, 0, 0))
    Boom.append(boomy)

img_mus = path.join(path.dirname(__file__), 'Music')
pygame.mixer.music.load(path.join(img_mus, 'tgfcoder-FrozenJam-SeamlessLoop.mp3'))
pygame.mixer.music.play(loops=-1)
pygame.mixer.music.set_volume(0.4)
shoot_mus = pygame.mixer.Sound(path.join(img_mus, 'pew.wav'))
boom = pygame.mixer.Sound(path.join(img_mus, 'expl3.wav'))


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = fon_player
        self.image.set_colorkey((0, 0, 0))
        self.hp_pl = 300
        self.rect = self.image.get_rect()
        self.rect.centerx = width / 2
        self.rect.bottom = height
        self.speedx = 0

    def update(self):
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -35
            self.rect.x = self.rect.x + self.speedx
        if keystate[pygame.K_RIGHT]:
            self.speedx = 35
            self.rect.x = self.rect.x + self.speedx
        if self.rect.right > width:
            self.rect.right = width
        if self.rect.left < 0:
            self.rect.left = 0


class Meteors(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        index = random.randrange(0, 10)
        self.image_orig = fonmetr[index]
        self.image_orig.set_colorkey((0, 0, 0))
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randrange(0, width)
        self.rect.bottom = random.randrange(-30, -1)
        self.speedx = random.randrange(-3, 3)
        self.speedy = random.randrange(0, 8)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()

    def vrashalka(self):
        now = pygame.time.get_ticks()
        if now - self.last_update >= 50:
            self.rot = self.rot + self.rot_speed
            self.rot = self.rot % 360
            self.last_update = now
            image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.vrashalka()
        self.rect.x = self.rect.x + self.speedx
        self.rect.y = self.rect.y + self.speedy
        if self.rect.right > width:
            self.rect.centerx = random.randrange(0, width)
            self.rect.bottom = random.randrange(-30, -1)
            self.speedx = random.randrange(-3, 3)
            self.speedy = random.randrange(0, 8)
        if self.rect.left < 0:
            self.rect.centerx = random.randrange(0, width)
            self.rect.bottom = random.randrange(-30, -1)
            self.speedx = random.randrange(-3, 3)
            self.speedy = random.randrange(0, 8)
        if self.rect.top > height:
            self.rect.centerx = random.randrange(0, width)
            self.rect.bottom = random.randrange(-30, -1)
            self.speedx = random.randrange(-3, 3)
            self.speedy = random.randrange(0, 8)


class Pula(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = fon_pula
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -50

    def update(self):
        self.rect.y = self.rect.y + self.speedy
        if self.rect.top < 0:
            self.kill()


def printux(textux, widthux, heightux, razux):
    fontux = pygame.font.match_font('arial')
    fontux = pygame.font.Font(fontux, razux)
    textux = fontux.render(textux, True, ((255, 255, 255)))
    rectux = textux.get_rect()
    rectux.centerx = widthux
    rectux.centery = heightux
    screen.blit(textux, rectux)


def Health():
    BAR_L = 300
    BAR_H = 50
    out = pygame.Rect(100, 70, BAR_L, BAR_H)
    inside = pygame.Rect(102, 72, player.hp_pl, BAR_H - 4)
    pygame.draw.rect(screen, (255, 255, 0), inside)
    pygame.draw.rect(screen, (255, 255, 255), out, 2)


def game_over():
    dlc = True
    screen.blit(fon, fon_rect)
    while dlc:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                restart()
                dlc = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                dlc = False
                pygame.quit()
        screen.blit(fon, fon_rect)
        printux('WASTED', width / 2, height / 2, 100)
        printux('Press R to restart the game', width / 2, height / 2 + 100, 80)
        pygame.display.flip()


def restart():
    global colvo, meteor_move, all_sprites, cucha_pulek, player
    colvo = 0
    meteor_move = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    cucha_pulek = pygame.sprite.Group()
    player = Player()
    all_sprites.add(player)
    for m in range(0, 100):
        meteor = Meteors()
        all_sprites.add(meteor)
        meteor_move.add(meteor)


colvo = 0
meteor_move = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
cucha_pulek = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for m in range(0, 100):
    meteor = Meteors()
    all_sprites.add(meteor)
    meteor_move.add(meteor)
last_update = pygame.time.get_ticks()
bes = True
boomban = 0
while bes == True:
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            bes = False
            pygame.quit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            shoot_mus.play()
            ogon = Pula(player.rect.centerx, player.rect.top)
            all_sprites.add(ogon)
            cucha_pulek.add(ogon)
    hits = pygame.sprite.spritecollide(player, meteor_move, True)
    for hit in hits:
        player.hp_pl = player.hp_pl - hit.rect.width // 5
        if player.hp_pl < 0:
            player.hp_pl = 0
            game_over()
        meteor = Meteors()
        all_sprites.add(meteor)
        meteor_move.add(meteor)
    strelba = pygame.sprite.groupcollide(meteor_move, cucha_pulek, True, True)
    for strelban in strelba:
        ##        while boomban!=8:
        now = pygame.time.get_ticks()
        if now - last_update >= 100:
            boomban = boomban + 1
            print(boomban)
            strelban.image = Boom[boomban]
            strelban.speedx = 0
            strelban.speedy = 0
            last_update = now
        if boomban == 7:
            strelban.kill()
            print(1)
            boomban = 0
        boom.play()
        colvo = colvo + abs(106 - strelban.rect.width) // 2
        meteor = Meteors()
        all_sprites.add(meteor)
        meteor_move.add(meteor)
    screen.fill((0, 0, 0))
    screen.blit(fon, fon_rect)
    all_sprites.update()
    all_sprites.draw(screen)
    printux(str(colvo), width / 2, 70, 100)
    Health()
    pygame.display.flip()
