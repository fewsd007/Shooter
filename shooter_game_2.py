from pygame import *
from random import randint
from time import time as timer

goal = randint(11,50)
max_lost = randint(3,10)


#фоновая музыка
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

#шрифты и надписи
font.init()
font1 = font.SysFont('Commic Sans', 80)
win = font1.render('YOU WIN!', True, (188, 196, 27))

font2 = font.SysFont('Arial', 36)

# нам нужны такие картинки:
img_back = "galaxy.jpg" # фон игры
img_hero = "rocket.png" # герой
img_bullet = "bullet.png" # пуля
img_enemy = "ufo.png" # враг
img_aster = "asteroid.png" #астероид
load = 'loadjpg.jpg'

score = 0 # сбито кораблей
lost = 0 # пропущено кораблей
max_lost = 3 # проиграли, если пропустили столько
life = 3 # уровень здоровья

# класс-родитель для других спрайтов
class GameSprite(sprite.Sprite):
  # конструктор класса
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # Вызываем конструктор класса (Sprite):
        sprite.Sprite.__init__(self)

        # каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed

        # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
 
  # метод, отрисовывающий героя на окне
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# класс главного игрока
class Player(GameSprite):
    # метод для управления спрайтом стрелками клавиатуры
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_height - 100:
            self.rect.y += self.speed
  # метод "выстрел" (используем место игрока, чтобы создать там пулю)
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

# класс спрайта-врага   
class Enemy(GameSprite):
    # движение врага
    def update(self,lol):
        self.rect.y += self.speed
        global lost
        # исчезает, если дойдет до края экрана
        if self.rect.y > win_height and lol == 1:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1
        else:
            pass

# класс спрайта-пули   
class Bullet(GameSprite):
    # движение врага
    def update(self):
        self.rect.y += self.speed
        # исчезает, если дойдет до края экрана
        if self.rect.y < 0:
            self.kill()

# Создаем окошко
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))
loadline = transform.scale(image.load(load), (win_width, win_height))
# создаем спрайты
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)

monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 7))
    monsters.add(monster)

bullets = sprite.Group()


asteroids = sprite.Group()
for i in range(1,3):
    asteroid = Enemy(img_aster, randint(30, win_width-30), -40, 80, 50, randint(1,7))
    asteroids.add(asteroid)

# переменная "игра закончилась": как только там True, в основном цикле перестают работать спрайты
finish = False
# Основной цикл игры:
run = True # флаг сбрасывается кнопкой закрытия окна
rel_time= False
num_fire = 0


while run:
    # событие нажатия на кнопку Закрыть
    for e in event.get():
        if e.type == QUIT:
            run = False
        # событие нажатия на пробел - спрайт стреляет
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire += 1
                    fire_sound.play()
                    ship.fire()
                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True
    lose = font1.render('YOU LOSE!', True, (randint(25,255), randint(25,255), randint(25,255)))
    if not finish:
        # обновляем фон
        window.blit(background,(0,0))

        # пишем текст на экране
        text = font2.render("Счет: " + str(score), 1, (255, 255, 255))
        window.blit(text, (30, 50))

        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (30, 75))

        # производим движения спрайтов
        ship.update()
        monsters.update(1)
        asteroids.update(0)
        bullets.update()

        # обновляем их в новом местоположении при каждой итерации цикла
        ship.reset()
        monsters.draw(window)
        asteroids.draw(window)
        bullets.draw(window)

        #reload
        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 3:
                reload = font2.render('Wait, reload...',1,(150,0,0))
                window.blit(reload,(260,460))
            else:
                num_fire = 0
                rel_time = False


        collides = sprite.groupcollide(monsters,bullets,True,True)
        for c in collides:
            score += 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5)) 
            monsters.add(monster)

        if life <= 0 or lost >= max_lost: 
            finish = True # проиграли, ставим фон и больше не управляем спрайтами. 
            window.blit(lose, (200, 200))

        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False): 
            sprite.spritecollide(ship,monsters,True)
            sprite.spritecollide(ship,asteroids,True)
            life -= 1

        if score >= goal:
            finish = True
            window.blit(win, (200, 200))

        if life == 3:
            life_color = (0,150,0)
        if life == 2:
            life_color = (150,150,0)
        if life == 1:
            life_color = (150,0,0)

        text_life = font1.render(str(life),1,life_color)
        window.blit(text_life,(650,10))

        display.update()

    else:
        finish = False
        score = 0
        lost = 0
        num_fire = 0
        life = 3
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        for a in asteroids:
            a.kill()
        
        window.blit(loadline,(0,0))

        time.delay(3000)

        for i in range(1, 6):
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 7))
            monsters.add(monster)
        for i in range(1,3):
            asteroid = Enemy(img_aster, randint(30, win_width-30), -40, 80, 50, randint(1,7))
            asteroids.add(asteroid)

    # цикл срабатывает каждую 0.05 секунд
    time.delay(50)