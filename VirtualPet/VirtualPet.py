import sys, pickle,datetime
from PyQt5 import QtCore, QtCore, QtGui, QtPrintSupport , QtWidgets, uic

formclass, baseclass = uic.loadUiType("mainwindow.ui")

class MyForm(baseclass, formclass):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.actionStop.triggered.connect(self.stop_Click)  #将事件处理器连接到工具条按钮
        self.actionFeed.triggered.connect(self.feed_Click)
        self.actionWalk.triggered.connect(self.walk_Click)
        self.actionPlay.triggered.connect(self.play_Click)
        self.actionDoctor.triggered.connect(self.doctor_Click)
        self.doctor = False         #初始化处理
        self.walking = False
        self.sleeping = False
        self.playing = False
        self.eating = False
        self.time_cycle = 0
        self.hunger = 0
        self.happiness  = 8
        self.health = 8
        self.forceAwake = False
        self.sleepImages = ["sleep1.gif","sleep2.gif","sleep3.gif", "sleep4.gif"]  # 用于动画的列表图像
        self.eatImages = ["eat1.gif", "eat2.gif"]                                  # 
        self.walkImages = ["walk1.gif", "walk2.gif", "walk3.gif", "walk4.gif"]     #
        self.playImages = ["play1.gif", "play2.gif"]                               #
        self.doctorImages = ["doc1.gif", "doc2.gif"]                               #
        self.nothingImages  = ["pet1.gif", "pet2.gif", "pet3.gif"]                 #

        self.imageList = self.nothingImages
        self.imageIndex = 0

        self.myTimer1 = QtCore.QTimer(self)          # 设置定时器
        self.myTimer1.start(500)
        self.myTimer1.timeout.connect(self.animation_timer)

        self.myTimer2 = QtCore.QTimer(self)         
        self.myTimer2.start(5000)
        self.myTimer2.timeout.connect(self.tick_timer)

        filehandle = True
        try:                                                   # 尝试打开pickle文件
            file = open("savedata_vp.pkl", "r").decode('utf-8')                 # 转换为字符型
        except:
            filehandle = False
        if filehandle:
            save_list = pickle.load(file)  #如果文件打开，从pickle文件读取
            file.close()
        else:
            save_list = [8, 8, 0, datetime.datetime.now(), 0]   #如果pickle文件没有打开，使用默认值
        self.happiness = save_list[0]     #从列表取单个值
        self.health    = save_list[1]
        self.hunger    = save_list[2]
        timestamp_then = save_list[3]
        self.time_cycle = save_list[4]

        difference = datetime.datetime.now() - timestamp_then
        ticks = int(difference.seconds / 50)
        for i in range(0, ticks):
            self.time_cycle += 1
            if self.time_cycle == 60:
                self.time_cycle = 0
            if self.time_cycle <= 48:         #醒着
                self.sleeping = False
                if self.hunger < 8:
                    self.hunger += 1
            else:                            #睡觉
                self.sleeping = True
                if self.hunger < 8 and self.time_cycle % 3 == 0:
                    self.hunger += 1
            if self.hunger == 7 and (self.time_cycle % 2 ==0) and self.health > 0:
                self.health -= 1
            if self.hunger == 8 and self.health > 0:
                self.health -=1
        if self.sleeping:   #使用正确的动画，醒着或者在睡觉
            self.imageList = self.sleepImages
        else:
            self.imageList = self.nothingImages
        

    def sleep_test(self):    #做动作之前检查是否在睡觉
        if self.sleeping:
            result = (QtGui.QMessageBox.warning(self, 'WARNING',              #对话类型 使用警告信息对话框
"Are you sure you want to wake your pet up?  He'll be unhappy about it!",    
                    QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,             #要显示的按钮
                    QtGui.QMessageBox.No))     #默认按钮

            if result == QtGui.QMessageBox.Yes:
                self.sleeping = False
                self.happiness -= 4
                self.forceAwake = True
                return True
            else:
                return False
        else:
            return True


    def doctor_Click(self):     #医生按钮事件处理器
        if self.sleep_test():
            self.imageList = self.doctorImages
            self.doctor = True
            self.walking = False
            self.eating = False
            self.playing = False

    def feed_Click(self):      #喂养按钮事件处理器
        if self.sleep_test():
            self.imageList = self.eatImages
            self.eating = True
            self.walking = False
            self.playing = False
            self.doctor = False

    def play_Click(self):       #玩耍按钮事件处理器
        if self.sleep_test():
            self.imageList = self.playImages
            self.playing = True
            self.walking = False
            self.eating = False
            self.doctor = False

    def walk_Click(self):      #走路按钮事件处理器
        if self.sleep_test():
            self.imageList = self.walkImages
            self.walking = True
            self.eating = False
            self.playing = False
            self.doctor = False

    def stop_Click(self):      #停止按钮事件处理器
        if not self.sleeping:
            self.imageList = self.nothingImages
            self.walking = False
            self.eating = False
            self.playing = False
            self.doctor = False


#动画定时器事件（第0.5秒）处理器
    def animation_timer(self):
        if self.sleeping and not self.forceAwake:
            self.imageList = self.sleepImages
        self.imageIndex += 1
        if self.imageIndex >= len(self.imageList):
            self.imageIndex = 0
        icon = QtGui.QIcon()
        current_image = self.imageList[self.imageIndex]           #更新宠物图像
        icon.addPixmap(QtGui.QPixmap(current_image),              #
                       QtGui.QIcon.Disabled, QtGui.QIcon.Off)     #
        self.petPic.setIcon(icon)
        self.progressBar_1.setProperty("value", (8-self.hunger)*(100/8.0))
        self.progressBar_2.setProperty("value", self.happiness*(100/8.0))
        self.progressBar_3.setProperty("value", self.health*(100/8.0))


    def tick_timer(self):         #5秒定时器事件处理器开始
        self.time_cycle += 1
        if self.time_cycle == 60:
            self.time_cycle = 0
        if self.time_cycle <= 48 or self.forceAwake:   # 检查在睡觉还是醒着      
            self.sleeping = False
        else:
            self.sleeping = True                            
        if self.time_cycle == 0:
            self.forceAwake = False

        if self.doctor:          #根据活动增加或减少单位
            self.health += 1
            self.hunger += 1
        elif self.walking and (self.time_cycle % 2 == 0):
            self.happiness += 1
            self.health += 1
            self.hunger += 1
        elif self.playing:
            self.happiness += 1
            self.hunger += 1
        elif self.eating:
            self.hunger -= 2
        elif self.sleeping:
            if self.time_cycle % 3 == 0:
                self.hunger += 1
        else: 
            self.hunger += 1
            if self.time_cycle % 2 == 0:
                self.happiness -= 1
        if self.hunger > 8:  self.hunger = 8             #确保值没有越界
        if self.hunger < 0:  self.hunger = 0
        if self.hunger == 7 and (self.time_cycle % 2 ==0) :
            self.health -= 1
        if self.hunger == 8:
            self.health -=1
        if self.health > 8:  self.health = 8
        if self.health < 0:  self.health = 0
        if self.happiness > 8:  self.happiness = 8
        if self.happiness < 0:  self.happiness = 0
        self.progressBar_1.setProperty("value", (8-self.hunger)*(100/8.0))    #更新计量器
        self.progressBar_2.setProperty("value", self.happiness*(100/8.0))
        self.progressBar_3.setProperty("value", self.health*(100/8.0))

    # 将状态和时间戳保存到pickle文件
    def closeEvent(self, event):
        file = open("savedata_vp.pkl", "w")
        save_list = [self.happiness, self.health, self.hunger, datetime.datetime.now(), self.time_cycle]
        pickle.dump(save_list, file)
        event.accept()

    def menuExit_selected(self):
        self.close()

app = QtWidgets.QApplication(sys.argv)
myapp = MyForm()
myapp.show()
app.exec_()

