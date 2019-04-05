# -*- coding: utf-8 -*-
import os, sys

"""
    一笔画完小游戏脚本
    以左下角坐标为原点建立坐标系，返回路径数组
"""


road = []

def createMap(x_length, y_length, roadblock):
    road_map = []
    for i in range(0, x_length):
        for j in range(0, y_length):
            road_map.append((i, j))

    for k in roadblock:
        block_num = int(k)
        div, mod = divmod(int(block_num), x_length)
        if mod == 0:
            mod = x_length
            div = div - 1
        block_position = (mod - 1, y_length - div - 1)
        road_map.remove(block_position)
    return road_map

def init(coordinate, roadblock, start_block_num):
    start_block_num = int(start_block_num)
    x = int(coordinate[0])
    y = int(coordinate[1])
    all_position = createMap(x, y, roadblock)
    div, mod = divmod(int(start_block_num), x)
    if mod == 0:
        mod = x
        div = div - 1
    start_position = (mod - 1, y - div - 1)

    return all_position, start_position

def step(now_pool, position):
    position_pool = [i for i in now_pool]

    if position in position_pool:
        if len(position_pool) == 1 and position[0] == position_pool[0][0] and position[1] == position_pool[0][1]:
            return True

        # 走到position的坐标
        position_pool.remove(position)

        next_position = (position[0] + 1, position[1])
        one = step(position_pool, next_position)
        if one:
            road.append(next_position)
            return True

        next_position = (position[0] - 1, position[1])
        two = step(position_pool, next_position)
        if two:
            road.append(next_position)
            return True

        next_position = (position[0], position[1] + 1)
        three = step(position_pool, next_position)
        if three:
            road.append(next_position)
            return True

        next_position = (position[0], position[1] - 1)
        four = step(position_pool, next_position)
        if four:
            road.append(next_position)
            return True

def draw(road):
    pass

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print('参数太少')
        exit(-1)
    coordinate = sys.argv[1:3]
    if len(sys.argv) != 4:
        roadblock = sys.argv[3:-1]
    else:
        roadblock = []
    start_block_num = int(sys.argv[-1])
    all_position, start_position = init(coordinate, roadblock, start_block_num)
    step(all_position, start_position)
    # draw(road)
    length = len(road)
    for i in range(0, length):
        print(road[length - i - 1])
