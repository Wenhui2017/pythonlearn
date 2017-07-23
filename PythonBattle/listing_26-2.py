class AI:
    def __init__(self):
        pass
    def turn(self):
        if self.robot.lookInFront() == "bot":
            self.robot.attack()
        else:
            self.goTowards(self.robot.locateEnemy()[0])
    def goTowards(self,enemyLocation):
        myLocation = self.robot.position
        delta = (enemyLocation[0]-myLocation[0],enemyLocation[1]-myLocation[1])  #目标位置和机器人位置的差距
        if abs(delta[0]) > abs(delta[1]):
            if delta[0] < 0:
                targetOrientation = 3 #面向左
            else:
                targetOrientation = 1 #面向右
        else:
            if delta[1] < 0:
                targetOrientation = 0 #面向上
            else:
                targetOrientation = 2 #面向下
        if self.robot.rotation == targetOrientation:  #如果已经面向这个方向，就沿着这个方向走
            self.robot.goForth()
        else:                                         #否则就找到正确的方向
            leftTurnsNeeded = (self.robot.rotation - targetOrientation) % 4   #要知道正确的方向需要左转多少次
            if leftTurnsNeeded <= 2:   #如果要左转两次以上，则可以只右转一次
                self.robot.turnLeft()
            else:
                self.robot.turnRight()
