# -*- coding: utf-8 -*-
import os
import sys

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

    return x, y, all_position, start_position


def step(current_pool, position):
    position_pool = [i for i in current_pool]

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


def draw(x, y, position_pool, road):
    arrow = {
        'origin': 'O',
        'left_arrow': '\u2190',
        'up_arrow': '\u2191',
        'right_arrow': '\u2192',
        'down_arrow': '\u2193',
        'destination': 'X'
    }
    length = len(road)
    road_map = [road[length - i - 1] for i in range(0, length)]
    direction = {}
    pre = road_map[0]
    pool = [(i[0]*2, i[1]*2) for i in position_pool]
    for i in range(0, length):
        if pre[0] != road_map[i][0]:
            if pre[0] > road_map[i][0]:
                direction[(road_map[i][0]*2+1, road_map[i][1]*2)] = arrow['left_arrow']
            else:
                direction[(road_map[i][0]*2-1, road_map[i][1]*2)] = arrow['right_arrow']
        elif pre[1] > road_map[i][1]:
            direction[(road_map[i][0]*2, road_map[i][1]*2+1)] = arrow['down_arrow']
        elif pre[1] < road_map[i][1]:
            direction[(road_map[i][0]*2, road_map[i][1]*2-1)] = arrow['up_arrow']
        else:
            direction[(road_map[i][0]*2, road_map[i][1]*2)] = arrow['origin']
        if i == length - 1:
            direction[(road_map[i][0]*2, road_map[i][1]*2)] = arrow['destination']
        pre = road_map[i]

    for i in range(0, 2*y):
        for j in range(0, 2*x):
            if (j, 2*y-i-1) in direction:
                print(direction[(j, 2*y-i-1)].encode('utf-8').decode('utf-8'), end=' ')
            elif (j, 2*y-i-1) in pool:
                print('*'.encode('utf-8').decode('utf-8'), end=' ')
            else:
                print(' ', end=' ')
        print()


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
    x, y, all_position, start_position = init(coordinate, roadblock, start_block_num)
    step(all_position, start_position)
    road.append(start_position)
    draw(x, y, all_position, road)
