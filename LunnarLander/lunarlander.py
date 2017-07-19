import pygame, sys

pygame.init()                                   
screen = pygame.display.set_mode([400,600])    #初始化游戏，做好一切准备，建立窗口
screen.fill([0, 0, 0])   #用白色填充窗口
ship = pygame.image.load('lunarlander.png') #加载图片
moon = pygame.image.load('moonsurface.png')
ground  = 540   #降落点是y = 540
start = 90
clock = pygame.time.Clock() #控制帧速率
ship_mass = 5000.0
fuel = 5000.0
velocity = -100.0
gravity = 10
height = 2000
thrust = 0
delta_v = 0
y_pos = 90
held_down = False


class ThrottleClass(pygame.sprite.Sprite): #推进器的精灵类
    def __init__(self, location = [0,0]):
        pygame.sprite.Sprite.__init__(self)  
        image_surface = pygame.surface.Surface([30, 10])  #创建一个30*10像素的surface
        image_surface.fill([128,128,128])  #填充颜色
        self.image = image_surface.convert()  #修改图像（Surface对象）的像素格式
        self.rect = self.image.get_rect()  #获取self.image大小
        self.rect.left, self.rect.centery = location


def calculate_velocity(): #计算高度，速度，加速度，燃料
    global thrust, fuel, velocity, delta_v, height, y_pos
    delta_t = 1/fps   #“滴答”对应Pygame循环的一帧
    thrust = (500 - myThrottle.rect.centery) * 5.0   #将推进器精灵的y位置转换为推力
    fuel -= thrust /(10 * fps)  #根据推力的多少减少燃料             
    if fuel < 0:  fuel = 0.0
    if fuel < 0.1:  thrust = 0.0
    delta_v = delta_t * (-gravity + 200 * thrust / (ship_mass + fuel))  #物理公式
    velocity = velocity + delta_v
    delta_h = velocity * delta_t
    height = height + delta_h
    y_pos = ground - (height * (ground - start) / 2000) - 90  #将高度转换为Pygame的y位置

    
def display_stats():  #使用字体显示信息
    v_str = "velocity: %i m/s" % velocity
    h_str = "height:   %.1f" % height
    t_str = "thrust:   %i" % thrust
    a_str = "acceleration: %.1f" % (delta_v * fps)
    f_str = "fuel:  %i" % fuel  
    v_font = pygame.font.Font(None, 26)  # 创建一个字体对象 none为默认字体 
    v_surf = v_font.render(v_str, 1, (255, 255, 255))  #用render方法来绘制文本
    screen.blit(v_surf, [10, 50])  #显示字体对象
    a_font = pygame.font.Font(None, 26)
    a_surf = a_font.render(a_str, 1, (255, 255, 255))
    screen.blit(a_surf, [10, 100])
    h_font = pygame.font.Font(None, 26)
    h_surf = h_font.render(h_str, 1, (255, 255, 255))
    screen.blit(h_surf, [10, 150])
    t_font = pygame.font.Font(None, 26)
    t_surf = t_font.render(t_str, 1, (255, 255, 255))
    screen.blit(t_surf, [10, 200])  
    f_font = pygame.font.Font(None, 26)
    f_surf = f_font.render(f_str, 1, (255, 255, 255))
    screen.blit(f_surf, [60, 300])

  
def display_flames():  #使用两个三角形表示火焰尾焰
    flame_size = thrust / 15
    for i in range (2):
        startx = 252 - 10 + i * 19
        starty = y_pos + 83
        pygame.draw.polygon(screen, [255, 109, 14], [(startx, starty), 
                                 (startx + 4, starty + flame_size), 
                                 (startx + 8, starty)], 0)  #画出三角形


def display_final():  #游戏结束时显示最终的统计信息
    final1 = "Game over"
    final2 = "You landed at %.1f m/s" % velocity
    if velocity > -5:
        final3 = "Nice landing!"
        final4 = "I hear NASA is hiring!"
    elif velocity > -15:
        final3 = "Ouch!  A bit rough, but you survived."
        final4 = "You'll do better next time."
    else:
        final3 = "Yikes!  You crashed a 30 Billion dollar ship."
        final4 = "How are you getting home?"
    pygame.draw.rect(screen, [0, 0, 0], [5, 5, 350, 280],0)  
    f1_font = pygame.font.Font(None, 70)
    f1_surf = f1_font.render(final1, 1, (255, 255, 255))
    screen.blit(f1_surf, [20, 50])   
    f2_font = pygame.font.Font(None, 40)
    f2_surf = f2_font.render(final2, 1, (255, 255, 255))
    screen.blit(f2_surf, [20, 110]) 
    f3_font = pygame.font.Font(None, 26)
    f3_surf = f3_font.render(final3, 1, (255, 255, 255))
    screen.blit(f3_surf, [20, 150]) 
    f4_font = pygame.font.Font(None, 26)
    f4_surf = f4_font.render(final4, 1, (255, 255, 255))
    screen.blit(f4_surf, [20, 180]) 
    pygame.display.flip()

myThrottle = ThrottleClass([15, 500])  #创建推进器对象


running = True
while running:  #主Pygame事件循环开始
    clock.tick(30)
    fps = clock.get_fps()
    if fps < 1:  fps = 30
    if height > 0.01:    
        calculate_velocity()
        screen.fill([0, 0, 0])
        display_stats()
        pygame.draw.rect(screen, [0, 0, 255], [80, 350, 24, 100], 2)  #画出燃料表轮廓
        fuelbar = 96 * fuel / 5000 
        pygame.draw.rect(screen, [0,255,0], [84,448-fuelbar,18, fuelbar], 0)#燃油量
        pygame.draw.rect(screen, [255, 0, 0], [25, 300, 10, 200], 0) #画出推进器滑块
        screen.blit(moon, [0, 500, 400, 100])    #画出月球                     
        pygame.draw.rect(screen, [60, 60, 60], [220, 535, 70, 5], 0)  #降落点
        screen.blit(myThrottle.image, myThrottle.rect)              
        display_flames()                                             
        screen.blit(ship, [230, y_pos, 50, 90]) #画出飞船                    
        instructions1 = "Land softly without running out of fuel"
        instructions2 = "Good landing: < 15 m/s    Great landing:  < 5m/s"
        inst1_font = pygame.font.Font(None, 24)
        inst1_surf = inst1_font.render(instructions1, 1, (255, 255, 255))
        screen.blit(inst1_surf, [50, 550])
        inst2_font = pygame.font.Font(None, 24)
        inst2_surf = inst1_font.render(instructions2, 1, (255, 255, 255))
        screen.blit(inst2_surf, [20, 575])
        pygame.display.flip()  
    
    else:  
        display_final()  #游戏结束，打印最终得分
                  
    for event in pygame.event.get():  #检查鼠标是否拖动推进器
        if event.type == pygame.QUIT: 
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:          
            held_down = True                                
        elif event.type == pygame.MOUSEBUTTONUP:            
            held_down = False                               
        elif event.type == pygame.MOUSEMOTION:
            if held_down:
                myThrottle.rect.centery = event.pos[1]  #更新推进器的位置
                if myThrottle.rect.centery < 300:
                    myThrottle.rect.centery = 300
                if myThrottle.rect.centery > 500:
                    myThrottle.rect.centery = 500
pygame.quit()

