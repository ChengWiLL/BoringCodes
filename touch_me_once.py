# -*- coding: utf-8 -*-

"""
    一笔画完小游戏脚本
    :parameter 终点坐标和一个包含所有可移动位置坐标的数组
    :return 移动路径数组

"""

all_position = [(-2, 2), (-1, 2), (0, 2), (1, 2), (2, 2),
                (-2, 1), (-1, 1), (0, 1), (1, 1), (2, 1),
                (-2, 0), (-1, 0), (1, 0), (2, 0),
                (-2, -1), (-1, -1), (0, -1), (1, -1), (2, -1)]

road = []


def step(position, now_pool):
    position_pool = [i for i in now_pool]

    if position in position_pool:
        if len(position_pool) == 1 and position[0] == 1 and position[1] == 0:
            return True

        # 走到position的坐标
        position_pool.remove(position)

        next_position = (position[0] + 1, position[1])
        one = step(next_position, position_pool)
        if one:
            road.append(next_position)
            return True

        next_position = (position[0] - 1, position[1])
        two = step(next_position, position_pool)
        if two:
            road.append(next_position)
            return True

        next_position = (position[0], position[1] + 1)
        three = step(next_position, position_pool)
        if three:
            road.append(next_position)
            return True

        next_position = (position[0], position[1] - 1)
        four = step(next_position, position_pool)
        if four:
            road.append(next_position)
            return True


if __name__ == "__main__":
    step((-1, 2), all_position)
    print(road)
