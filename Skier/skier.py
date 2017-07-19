import pygame, sys, random


skier_images = ["./resource/skier_down.png",
                "./resource/skier_right1.png", "./resource/skier_right2.png",
                "./resource/skier_left2.png", "./resource/skier_left1.png"]    #滑雪者的方向对应不同的图片

class SkierClass(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("./resource/skier_down.png")
        self.rect = self.image.get_rect()
        self.rect.center = [320, 100]
        self.angle = 0

    def turn(self, direction):
        self.angle = self.angle + direction
        if self.angle < -2:  self.angle = -2 #不让滑雪者的状态超过 +/-2
        if self.angle >  2:  self.angle =  2
        center = self.rect.center
        self.image = pygame.image.load(skier_images[self.angle])
        self.rect = self.image.get_rect()
        self.rect.center = center
        speed = [self.angle, 6-abs(self.angle) * 2]
        return speed

    def move(self, speed):                                        #左右移动滑雪者
        self.rect.centerx = self.rect.centerx + speed[0]
        if self.rect.centerx < 20:  self.rect.centerx = 20
        if self.rect.centerx > 620: self.rect.centerx = 620


class ObstacleClass(pygame.sprite.Sprite):  #创建单个障碍物
    def __init__(self, image_file, location, type):
        pygame.sprite.Sprite.__init__(self)
        self.image_file = image_file
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.center = location
        self.type = type
        self.passed = False

    def update(self):  #修改每个障碍物位置的y值，取决于滑下小山的速度
        global speed  #包括x和y方向的速度 使用索引[1]获取y方向的速度
        self.rect.centery -= speed[1]  
        if self.rect.centery < -32: #检查障碍物是否已移出屏幕
            self.kill()             #移出它

def create_map():  #创建障碍物地图
    global obstacles
    locations = []
    for i in range(10):  #每屏10个障碍物
        row = random.randint(0, 9)
        col = random.randint(0, 9)
        location = [col * 64 + 32, row * 64 +32 +640]  #障碍物的位置（x, y）， +640是希望障碍物从底部出现
        if not (location in locations):  #确保没有将同一个障碍物放入同一个位置
            locations.append(location)
            type = random.choice(["tree", "flag"])
            if type == "tree": img = "./resource/skier_tree.png"
            elif type == "flag": img = "./resource/skier_flag.png"
            obstacle = ObstacleClass(img, location, type)
            obstacles.add(obstacle)

def animate():                  #重绘屏幕
    screen.fill([255, 255, 255])
    obstacles.draw(screen)
    screen.blit(skier.image, skier.rect)
    screen.blit(score_text, [10, 10])
    pygame.display.flip()

pygame.init()
screen = pygame.display.set_mode([640, 640])
clock = pygame.time.Clock()
points = 0
speed = [0, 6]
obstacles = pygame.sprite.Group()
map_position = 0
create_map()
skier = SkierClass()
font = pygame.font.Font(None, 50)


running = True
while running:
    clock.tick(30)
    for event in pygame.event.get(): #检查按键事件
        if event.type == pygame.QUIT: running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT: #左方向键向左转
                speed = skier.turn(-1)
            elif event.key == pygame.K_RIGHT:  #右方向键向右转
                speed = skier.turn(1)
    skier.move(speed)
    
    map_position += speed[1]  #记录地图已经往上滚动了多少

    if map_position >= 640:  #如果整屏已经滚动完，创建一个新的含障碍物的场景
        create_map()         #
        map_position = 0     #

    hit = pygame.sprite.spritecollide(skier, obstacles, False) #使用spritecollide()函数进行碰撞检测
    if hit:
        if hit[0].type == "tree" and not hit[0].passed: #碰到树  变量hit告诉我们滑雪者撞到了哪个障碍物 是一个列表 一次只能碰到一个
            points = points - 10
            skier.image = pygame.image.load("./resource/skier_crash.png")  #显示碰撞后的图像
            animate()                                                      #
            pygame.time.delay(1000)                                        #
            skier.image = pygame.image.load("./resource/skier_down.png")   #继续滑雪
            skier.angle = 0                                                #
            speed = [0, 6]                                                 #
            hit[0].passed = True  #表示已经碰到了这棵树
            
        elif hit[0].type == "flag" and not hit[0].passed:  #捡到小旗
            points += 100                                  
            hit[0].kill()  #移除小旗

    obstacles.update()
    score_text = font.render("Score: " +str(points), 1, (0, 0, 0))
    animate()  #重绘屏幕

pygame.quit()
    

    
