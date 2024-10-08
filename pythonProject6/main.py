from pygame import *
from random import randint
from time import time as timer

font.init()
font1 = font.Font(None, 80)
win = font1.render('YOU WIN', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))

font2 = font.Font(None, 36)

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
fire_sound = mixer.Sound('fire.ogg')
mixer.music.set_volume(0.2)

img_back = 'galaxy.jpg'
img_hero = 'rocket.png'
img_enemy = 'ufo.png'
img_bullet = 'bullet.png'
img_asteroid = 'asteroid.png' # Изображение астероида

score = 0
lost = 0
max_lost = 3
goal = 10
lives = 3 # Количество жизней

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed

    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed;
        if self.rect.y < 0:
            self.kill()

class Asteroid(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__(player_image, player_x, player_y, size_x, size_y, player_speed)
        self.rect.x = randint(0, win_width - self.rect.width)
        self.rect.y = -self.rect.height

    def update(self):
        self.rect.y += self.speed
        global lives
        if self.rect.y > win_height:
            self.rect.x = randint(0, win_width - self.rect.width)
            self.rect.y = -self.rect.height
        if sprite.collide_rect(self, ship):
            self.rect.x = randint(0, win_width - self.rect.width)
            self.rect.y = -self.rect.height
            lives -= 1

win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)

monsters = sprite.Group()
bullets = sprite.Group()
asteroids = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), 0, 80, 50, randint(1, 5))
    monsters.add(monster)
for i in range(1, 4):
    asteroid = Asteroid(img_asteroid, 0, 0, 50, 50, randint(1, 5))
    asteroids.add(asteroid)

run = True
finish = False
matrix_effect = False
rel_time = False
num_fire = 0
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == MOUSEBUTTONDOWN:
            if num_fire < 5 and rel_time == False:
                num_fire = num_fire + 1
                fire_sound.play()
                ship.fire()

            if num_fire >= 5 and rel_time == False:
                last_time = timer()
                rel_time = True


    if not finish:
        window.blit(background, (0, 0))
        ship.update()
        bullets.update()
        monsters.update()
        asteroids.update()
        ship.reset()
        bullets.draw(window)
        monsters.draw(window)
        asteroids.draw(window)

        if rel_time == True:
            now_time = timer()

            if now_time - last_time < 2:
                reload = font2.render('Wait, reload....', 1, (150, 0, 0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0
                rel_time = False

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        if sprite.spritecollide(ship, monsters, False) or lost >= max_lost or lives == 0:
            finish = True
            window.blit(lose, (200, 200))

        if score >= goal:
            finish = True
            window.blit(win, (200, 200))

        text = font2.render('Счет: ' + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render('Пропущено:' + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        text_lives = font2.render('Жизни: ' + str(lives), 1, (255, 255, 255))
        window.blit(text_lives, (10, 80))

        display.update()

    time.delay(50)