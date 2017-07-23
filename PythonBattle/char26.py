class AI:  #等待CircleAI绕圈，等它在前方时攻击它，前提是知道CircleAI的工作方式，引发次其它机器人不能打败
    def __init__(self):
        self.isFirstTurn = True
    def turn(self):
        if self.isFirstTurn:
            self.robot.turnLeft()
            self.isFirstTurn = False
            elif self.robot.lookInfont() == "bot":
                self.robot.attack()
            else:
                self.robot.doNothing()
