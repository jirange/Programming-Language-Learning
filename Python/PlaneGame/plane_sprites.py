import random
import pygame

"""游戏参数设置"""
BG_RECT = pygame.Rect(0, 0, 480, 700)  # 屏幕大小
FRAME_PER_SEC = 60  # 刷新帧率
CREATE_ENEMY_EVENT = pygame.USEREVENT  # 创建敌机的定时器常量
HERO_FIRE_EVENT = pygame.USEREVENT + 1  # 英雄发射子弹事件

AN_ENEMY_POINTS = 1  # 击毁一架敌机得1分
"""英雄参数"""
HERO_SPEED = 5  # 英雄左右移动速度（灵活性）
"""敌机参数"""
ENEMY_SPEED_LOW = 3  # 敌机速度下界
ENEMY_SPEED_HIGH = 4  # 敌机速度上界
ENEMY_CREATE_NUM = 3  # 1s内生成敌机个数
"""子弹参数"""
A_ROUND_BULLETS = 2  # 一轮连发子弹个数
BULLET_SPEED = 2  # 子弹移动速度
BULLET_CREATE_NUM = 2  # 1s内生成子弹个数


class GameSprite(pygame.sprite.Sprite):
    """飞机大战游戏精灵"""

    def __init__(self, image_name, speed=3):
        super().__init__()  # 调用父类的初始化方法

        # 定义对象的属性
        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()
        self.speed = speed

    def update(self, *args):
        self.rect.y += self.speed  # 在屏幕竖直方向上移动


class Background(GameSprite):
    """游戏背景精灵"""

    def __init__(self, is_alt=False):
        # 创建背景精灵
        super().__init__("./images/background.png")
        # 若为交替图像，则初始值应在屏幕窗口的上方
        if is_alt:
            self.rect.y = -self.rect.height
        pass

    def update(self):
        super().update()
        # 背景图像移出屏幕后，将图像设置到屏幕的上方（采用跑酷经典背景滚动方法）
        if self.rect.y >= BG_RECT.height:
            self.rect.y = -BG_RECT.height


class Enemy(GameSprite):
    """敌机精灵"""
    def __init__(self):
        # 1.创建敌机精灵，同时指定敌机图片
        super().__init__("./images/enemy1.png")
        # 2.指定敌机的初始随机速度
        self.speed = random.randint(ENEMY_SPEED_LOW, ENEMY_SPEED_HIGH)
        # 3.指定敌机的初始随机位置
        self.rect.x = random.randint(0, BG_RECT.width-self.rect.width)
        self.rect.bottom = 0  # bottom = y + height

    def update(self):
        # 1.保持垂直方向的飞行
        super().update()
        # 2.若飞出屏幕，从精灵组中删除敌机
        if self.rect.y >= BG_RECT.height:
            self.kill()  # kill方法可以将精灵从所有精灵组中移出，精灵会被自动销毁


class Hero(GameSprite):
    """英雄精灵"""
    def __init__(self):
        # 1.指定英雄图片，并设置速度为0
        super().__init__("./images/me1.png", speed=0)
        # 2.设置英雄初始位置
        self.rect.centerx = BG_RECT.centerx
        self.rect.bottom = BG_RECT.bottom - 120
        # 3.定义bullets子弹精灵组,保存子弹精灵
        self.bullets = pygame.sprite.Group()
        # 4.增加bullets属性,记录所有子弹精灵
        pass

    def update(self):
        # 1.英雄需要水平移动
        self.rect.x += self.speed
        # 2.需要保证不能移出屏幕
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > BG_RECT.width-self.rect.width:
            self.rect.right = BG_RECT.right  # right=x+width

    # 增加 fire 方法，用于发射子弹
    def fire(self):
        for i in range(1, A_ROUND_BULLETS+1):
            # 1.创建子弹精灵
            bullet = Bullet()
            # 2.设置精灵的位置
            bullet.rect.bottom = self.rect.y - i*20
            bullet.rect.centerx = self.rect.centerx
            # 3.将精灵添加到精灵组
            self.bullets.add(bullet)
    """def fire(self):
        # 1.创建子弹精灵
        bullet = Bullet()
        # 2.设置精灵的位置
        bullet.rect.bottom = self.rect.y - 20
        bullet.rect.centerx = self.rect.centerx
        # 3.将精灵添加到精灵组
        self.bullets.add(bullet)"""


class Bullet(GameSprite):
    def __init__(self):
        # 1.指定子弹图片，并设置初始速度为-2
        super().__init__("./images/bullet1.png", speed=-BULLET_SPEED)

    def update(self):
        # 子弹垂直方向飞行 调用父类方法
        super().update()
        # 判断子弹飞出屏幕,从精灵组中删除
        if self.rect.bottom < 0:
            self.kill()
