import pygame as pg
from pygame.locals import *

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 800
FPS = 60

PLAYER_STATES = {
    0: 'NORMAL',  # 正常飞行
    1: 'DAMAGED',  # 飞机受损
    2: 'INVINCIBLE',  # 飞机无敌
    3: 'ATTACKING'  # 飞机开火
}

ATTACK_STATES = {
    0: 'OFF',  # 关火
    1: 'BULLET',  # 普通子弹
    2: 'MISSILE',  # 导弹
    3: 'LASER'  # 激光
}


class Player:
    def __init__(self):
        self.state = 0
        self.attack_state = 0
        self.images = {
            'NORMAL': pg.image.load("./Images/player.png"),
            'DAMAGED': pg.image.load("./Images/playerhpdown.png"),
            'INVINCIBLE': pg.image.load("./Images/playerinvincible.png"),
            'ATTACKING': pg.image.load("./Images/playeratk.png")
        }
        self.bullet_image = pg.image.load("./Images/playerbullet1.png")
        self.position = [0, 0]

    def update(self, position):
        self.position = position

    def draw(self, screen):
        state_name = PLAYER_STATES[self.state]
        screen.blit(self.images[state_name], self.position)

    def attack(self, screen):
        if self.attack_state == 1:  # 普通子弹
            x, y = self.position
            for b in range(y, 0, -10):
                screen.blit(self.bullet_image, (x, b - 40))


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

    def draw(self):
        self.screen.fill((0, 0, 0))
        pg.draw.rect(self.screen, (255, 255, 255), (0, 0, WINDOW_WIDTH, WINDOW_HEIGHT))
        self.player.draw(self.screen)
        self.player.attack(self.screen)

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