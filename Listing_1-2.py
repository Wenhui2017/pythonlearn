import random
secret = random.randint(1, 99)     # 选一个秘密数
guess = 0
tries = 0
print ("AHOY!  I'm the Dread Pirate Roberts, and I have a secret!")
print ("It is a number from 1 to 99.  I'll give you 6 tries. ")

# 最多允许猜6次
while guess != secret and tries < 6:                
    guess = int(input("What's yer guess? "))   # 得到玩家猜的数
    if guess < secret:
        print ("Too low, ye scurvy dog!")
    elif guess > secret:
        print ("Too high, landlubber!")

    tries = tries + 1            # 用掉一次机会               

# 游戏结束时打印消息
if guess == secret:                           \
    print ("Avast! Ye got it!  Found my secret, ye did!")
else:
    print ("No more guesses!  Better luck next time, matey!")
    print ("The secret number was", secret)
