class AI:
    def __init__(self):  #在开始时创建机器人
        self.currentlyDoing = "forward"  #新属性让机器人记住现在正在做什么
    def turn(self):  #在每一回合都会被调用，决定机器人做什么
        if self.robot.lookInFront() == "bot":
            self.robot.attack()  #攻击
        elif self.robot.lookInFront() == "wall":
            self.robot.turnRight()  #转圈
            self.currentlyDoing = "turnRight"  #希望机器人能折返 两次右转 须记住当前做什么
        elif self.currentlyDoing == "turnRight":
            self.robot.turnRight()
            self.currentlyDoing = "forward"
        else:
            self.robot.goForth()
