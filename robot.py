#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 10:50:18 2019
"""

from map import Map
import math


###############################################################################
# Project 2:    Robot
# Due:          February 6, 2019
# Author(s):    Pamela Regudo, Florence Yao, Christopher Yip
# Description:  Robot cleans one 3x3 block before moving on to the next. Each
#              which has a "middle-point" stored in the "blocks" array. Only
#              after cleaning an entire block, then the robot moves on to the
#              next. The range is continuously checked after each step to ensure
#              the robot does not step out of bounds.
###############################################################################


class Robot:
    def __init__(self):
        self.start = (0, 0)
        self.track = [self.start]
        self.current = self.start

    def clean(self, task: Map):
        # init
        size = 19
        done = False
        right = True

        while (not done):
            x = math.floor(self.current[1] / 3) * 3 + 1
            y = math.floor(self.current[0] / 3) * 3 + 1
            if (y >= size):
                y -= 1
            if (x >= size):
                x -= 1
            current_mid = (y, x)

            task.dirty[self.current[0]][self.current[1]] = 0
            dirty_areas = self.get_dirty_areas(task)

            # start cleaning dirty spots around you
            # if nothing around you is dirty, go back to the middle
            while (dirty_areas):
                target = dirty_areas.pop()
                self.move(target)

                # clean
                task.dirty[self.current[0]][self.current[1]] = 0

                # update
                dirty_areas = self.get_dirty_areas(task)

            # if adjacent spots are clean from middle, move to next block
            if (self.current == current_mid):
                x = self.current[1]
                y = self.current[0]
                if (right):
                    if ((x + 2) >= size):
                        right = False
                        y += 2
                    else:
                        x += 2
                else:
                    if ((x - 2) < 0):
                        right = True
                        y += 2
                    else:
                        x -= 2
                if (y >= size):
                    done = True
                else:
                    target = (y, x)
                    self.move(target)
            else:  # if adjacent spots are clean, return to middle point of block
                self.move(current_mid)

    # gets dirty adjacent spots of robot
    # checks for out of range areas by mod operation
    def get_dirty_areas(self, task: Map):
        dirty_areas = []

        # if top row of 3x3 set lower to current row and upper to +2
        if (self.current[0] % 3 == 0):
            ilower = self.current[0]
            iupper = self.current[0] + 2
        # if middle row of 3x3 set lower to -1 and upper to +2
        elif (self.current[0] % 3 == 1):
            ilower = self.current[0] - 1
            iupper = self.current[0] + 2
        # if bottom row of 3x3 set lower to -1 and upper to +1
        else:
            ilower = self.current[0] - 1
            iupper = self.current[0] + 1

        if (iupper > 19):
            iupper -= 1

        if (self.current[1] % 3 == 0):
            jlower = self.current[1]
            jupper = self.current[1] + 2
        elif (self.current[1] % 3 == 1):
            jlower = self.current[1] - 1
            jupper = self.current[1] + 2
        else:
            jlower = self.current[1] - 1
            jupper = self.current[1] + 1

        if (jupper > 19):
            jupper -= 1

        # scan all adjacent spots of robot given above parameters
        for i in range(ilower, iupper):
            for j in range(jlower, jupper):
                if (task.dirty[i][j] == 1):
                    dirty_areas.append((i, j))
            j = self.current[1]  # reset

        return dirty_areas

    def move(self, point):
        while (self.current != point):
            # step northeast
            if ((self.current[0] > point[0]) & (self.current[1] < point[1])):
                self.current = (self.current[0] - 1, self.current[1] + 1)

            # step northwest
            elif ((self.current[0] > point[0]) & (self.current[1] > point[1])):
                self.current = (self.current[0] - 1, self.current[1] - 1)

            # step southeast
            elif ((self.current[0] < point[0]) & (self.current[1] < point[1])):
                self.current = (self.current[0] + 1, self.current[1] + 1)

            # step southwest
            elif ((self.current[0] < point[0]) & (self.current[1] > point[1])):
                self.current = (self.current[0] + 1, self.current[1] - 1)

            # step south
            elif (self.current[0] < point[0]):
                self.current = (self.current[0] + 1, self.current[1])

            # step north
            elif (self.current[0] > point[0]):
                self.current = (self.current[0] - 1, self.current[1])

            # step east
            elif (self.current[1] < point[1]):
                self.current = (self.current[0], self.current[1] + 1)

            # step west
            elif (self.current[1] > point[1]):
                self.current = (self.current[0], self.current[1] - 1)

            self.track.append(self.current)

            print(self.current)

    def show(self):
        print('Number of steps: ', len(self.track) - 1)


if __name__ == '__main__':
    home = Map(19, 19)
    home.show()
    agent = Robot()
    agent.clean(home)
    agent.show()
    home.show()