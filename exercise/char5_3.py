#第一小题
length = float(input("这个房间的长为： "))
width = float(input("这个房间的宽为： "))
price = float(input("每平方尺地毯的价格是多少？"))
area = length * width
print("这个房间共需要", area, "平方米的地毯。")

#第二小题
area_yards = area / 9.0
print("这个房间总共需要", area_yards, "平方尺。")

#第三小题
total_cost = price * area_yards
print("地毯总价格为", total_cost, "元")


