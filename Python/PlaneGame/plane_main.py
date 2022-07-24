import pygame
from plane_sprites import *


class PlaneGame:
    """飞机大战主游戏类"""

    # 游戏初始化
    def __init__(self):
        # 1.创建游戏窗口
        self.screen = pygame.display.set_mode(BG_RECT.size)
        # 2.创建游戏时钟
        self.clock = pygame.time.Clock()
        # 3.调用私有方法__create_sprites创建精灵和精灵组
        self.__create_sprites()
        # 4.设置定时器事件——创建敌机 1s (ms)
        pygame.time.set_timer(CREATE_ENEMY_EVENT, int(1000/ENEMY_CREATE_NUM))
        # 设置定时器事件——发射子弹
        pygame.time.set_timer(HERO_FIRE_EVENT, int(1000/BULLET_CREATE_NUM))

        # 音乐初始化
        pygame.init()
        pygame.mixer.init()
        self.hit_sound = pygame.mixer.Sound("./musics/bullet_hit.wav")
        self.fire_sound = pygame.mixer.Sound("./musics/bullet1.wav")

        # 分数初始化
        self.score = 0
        # self.font = pygame.font.Font('freesansbold.ttf', 20)  # 字体及大小参数设置
        self.font = pygame.font.SysFont('freesansbold', 40)
        # self.over_font = pygame.font.Font('freesansbold.ttf', 50)  # 字体及大小参数设置
        self.over_font = pygame.font.SysFont('freesansbold', 70)

    def __create_sprites(self):
        # 创建背景精灵和精灵组
        bg1 = Background()
        bg2 = Background(True)

        self.back_group = pygame.sprite.Group(bg1, bg2)
        # 创建敌机精灵组
        self.enemy_group = pygame.sprite.Group()
        # 创建英雄精灵和精灵组
        # 后续要对英雄做碰撞检测和发射子弹，故需单独定义成属性
        self.hero = Hero()
        self.hero_group = pygame.sprite.Group(self.hero)

    def show_score(self):
        """显示分数"""
        text = f"SCORE:{self.score}"
        score_render = self.font.render(text, True, (50, 50, 50))  # 分数颜色参数
        self.screen.blit(score_render, (10, 10))  # 分数位置参数

    def show_over(self):
        """显示游戏结束画面"""
        text = "GAME OVER!"
        score_render = self.over_font.render(text, True, (50, 50, 50))  # 颜色参数
        self.screen.blit(score_render, (90, BG_RECT.centery-50))  # 位置参数

    def start_game(self):
        # 游戏开始 -> 播放背景音乐
        pygame.mixer.music.load("./musics/bgm.wav")
        pygame.mixer.music.play(-1)

        # 游戏开始 -> 加载射中音效
        while True:
            # 1.设置刷新帧率
            self.clock.tick(FRAME_PER_SEC)
            # 2.事件监听
            self.__event_handler()
            # 3.碰撞检测
            self.__check_collide()
            # 4.更新/绘制精灵组
            self.__update_sprites()
            # 5.更新分数显示
            self.show_score()
            # 6.更新显示
            pygame.display.update()

    def __event_handler(self):
        for event in pygame.event.get():
            # 捕获 游戏退出操作
            if event.type == pygame.QUIT:
                PlaneGame.__game_over(self)
            # 捕获事件 定时创建敌机精灵并加入到相应精灵组
            elif event.type == CREATE_ENEMY_EVENT:
                enemy = Enemy()
                self.enemy_group.add(enemy)
            # 捕获事件 定时发射子弹
            elif event.type == HERO_FIRE_EVENT:
                self.hero.fire()
                self.fire_sound.play()

            """# 英雄移动
            # 用户必须要从键盘移开才算一次按键事件，灵活性降低
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT
                # TODO 向右移动"""
        # 捕获事件 英雄左右移动
        # 使用键盘提供的方法获取键盘按键-元组（按住方向键不放也可）
        keys_pressed = pygame.key.get_pressed()
        # 判断元组中对应的按键索引值 1
        if keys_pressed[pygame.K_RIGHT]:
            self.hero.speed = HERO_SPEED
        elif keys_pressed[pygame.K_LEFT]:
            self.hero.speed = -HERO_SPEED
        else:
            self.hero.speed = 0

    def __check_collide(self):
        # 子弹摧毁敌机
        collisions = pygame.sprite.groupcollide(self.hero.bullets, self.enemy_group, True, True)
        if collisions:
            self.score += AN_ENEMY_POINTS  # 游戏分数加1
            self.hit_sound.play()  # 播放射中音效
            print("%d" % self.score)

        # 敌机撞毁英雄,返回的是撞到英雄的敌机列表
        enemies = pygame.sprite.groupcollide(self.hero_group, self.enemy_group, True, False)
        if len(enemies) > 0:
            # 英雄牺牲
            """pygame.mixer.music.load("./musics/game_over.wav")
            pygame.mixer.music.play()"""
            self.hero.kill()
            self.__game_over()

    def __update_sprites(self):
        self.back_group.update()
        self.back_group.draw(self.screen)

        self.enemy_group.update()
        self.enemy_group.draw(self.screen)

        self.hero_group.update()
        self.hero_group.draw(self.screen)

        self.hero.bullets.update()
        self.hero.bullets.draw(self.screen)

    # @staticmethod
    def __game_over(self):
        # 播放英雄被击毁的音效
        pygame.mixer.music.load("./musics/game_over.wav")
        pygame.mixer.music.play()
        # 展示游戏结束提示
        self.show_over()
        pygame.display.update()
        pygame.time.wait(1000)
        print("GAME OVER!")
        print("YOUR SCORE: %d" % self.score)
        pygame.quit()  # quit 卸载所有的模块
        exit()


if __name__ == '__main__':

    # 建立游戏对象
    game = PlaneGame()
    game.start_game()
