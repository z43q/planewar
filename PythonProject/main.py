import os
import pygame as pg
from pygame.locals import *

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 800
FPS = 60

PLAYER_STATES = {
    0: 'NORMAL',    # 正常飞行
    1: 'DAMAGED',   # 飞机受损
    2: 'INVINCIBLE', # 飞机无敌
    3: 'ATTACKING'  # 飞机开火
}

ATTACK_STATES = {
    0: 'OFF',       # 关火
    1: 'BULLET',    # 普通子弹
    2: 'MISSILE',   # 导弹
    3: 'LASER'      # 激光
}
class Bullet:
    def __init__(self, x, y, speed=10, damage=1):
        self.x = x
        self.y = y
        self.speed = speed
        self.damage = damage
        self.is_alive = True
        # 加载子弹图片
        if os.path.exists("playerbullet1.png"): # 查找文件避免报错
            self.img = pg.image.load("playerbullet1.png")
            self.rect = self.img.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y

    def update(self):
        """更新子弹位置"""
        self.y -= self.speed
        self.rect.y = self.y
        if self.y < 0:
            self.is_alive = False

    def draw(self, screen):
        """绘制子弹"""
        if self.img:
            screen.blit(self.img, (self.x, self.y))


class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.state = 0
        self.attack_state = 0
        self.images = {
            'NORMAL': pg.image.load("player.png"),
            'DAMAGED': pg.image.load("playerhpdown.png"),
            'INVINCIBLE': pg.image.load("playerinvincible.png"),
            'ATTACKING': pg.image.load("playeratk.png")
        }
        self.bullet_image = pg.image.load("playerbullet1.png")
        self.position = [0, 0]
        # 子弹发射延迟
        self.shoot_delay = 300
        # 子弹冷却时间
        self.shoot_cooldown = 0
        # 储存发射的子弹
        self.bullets = []
        self.rect = self.images['NORMAL'].get_rect()

    def update(self, position=None):
        """更新玩家状态和位置"""
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        if position:
            self.position = position

    def shoot(self):
        """发射子弹"""
        if self.shoot_cooldown == 0:
            bullet = Bullet(self.rect.centerx - 2, self.rect.top)
            self.bullets.append(bullet)
            self.shoot_cooldown = self.shoot_delay

    def update_bullets(self):
        """更新所有子弹状态，移除无效子弹"""
        for bullet in self.bullets[:]:
            bullet.update()
            if not bullet.is_alive:
                self.bullets.remove(bullet)

    def draw_bullets(self, screen):
        """绘制所有子弹"""
        for bullet in self.bullets:
            bullet.draw(screen)

    def draw(self, screen):
        state_name = PLAYER_STATES[self.state]
        screen.blit(self.images[state_name], self.position)
class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pg.display.set_caption("像素飞机大战")
        pg.mouse.set_visible(False)
        self.clock = pg.time.Clock()
        self.running = True
        self.player = Player()

    def handle_events(self):
        for event in pg.event.get():
            if event.type == QUIT:
                self.running = False
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:  # 左键
                    self.player.state = 3
                    self.player.attack_state = 1

    def update(self):
        mouse_pos = pg.mouse.get_pos()
        self.player.update(mouse_pos)
        self.player.update_bullets()

    def draw(self):
        self.screen.fill((0, 0, 0))
        pg.draw.rect(self.screen, (255, 255, 255), (0, 0, WINDOW_WIDTH, WINDOW_HEIGHT))
        self.player.draw(self.screen)
        self.player.draw_bullets(self.screen)

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()

            pg.display.flip()
            self.clock.tick(FPS)
        pg.quit()
if __name__ == "__main__":
    game = Game()
    game.run()