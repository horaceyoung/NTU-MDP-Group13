from configurations import *
from vec2D import swap_coordinates
import time
class Exploration:
    def __init__(self, coverageLimit,timeLimit, robot, map):
        self.robot = robot
        self.map = map
        self.coverageLimit = coverageLimit
        self.timeLimit = timeLimit
        self.startTime = 0
        self.endTime = 0
        self.areaExplored = 0


    def runExploration(self):
        print("Starting Exploration...")
        self.startTime = time.time()
        self.endTime = self.startTime + self.timeLimit
        # self.areaExplored = self.calculateAreaExplored()  #Number of cells explored in grid
        print("Exploration Area: " + str(self.areaExplored))
        self.explorationLoop(self.bot.posRow,self.bot.posCol)


    def explorationLoop(self):
        while(True):
            self.next_move()
            # self.areaExplored = self.calculateAreaExplored()
            # print("Area Explored: " + str(self.areaExplored))
            # if(self.bot.posRow == r and self.bot.posCol == c):
            #     if(self.areaExplored >= 300):
            #         break
            # if(self.areaExplored >= self.coverageLimit or time.time() >= self.endTime):
            #     print("areaExplored, coverageLimit, curTime, endTime: ", self.areaExplored,self.coverageLimit,time.time(),self.endTime)
            #     break

    #Check if the direction relative to the robot has free space -
    @classmethod
    def look(cls, direction, robot, arena_map):
        print(robot.location)
        target_direction = robot.direction
        if direction == Direction.UP:
            pass
        elif direction == Direction.RIGHT:
            target_direction = target_direction.rotate(90).normalize()
        elif direction == Direction.LEFT:
            target_direction = target_direction.rotate(-90).normalize()
        direction_offset = target_direction.rotate(90).normalize()

        target_direction = swap_coordinates(target_direction)
        direction_offset = swap_coordinates(direction_offset)

        cell_coordinates = []  # cells to be looked
        cell_coordinates.append(pg.Vector2(robot.location + 2 * target_direction))
        cell_coordinates.append(pg.Vector2(robot.location + 2 * target_direction) + direction_offset)
        cell_coordinates.append(pg.Vector2(robot.location + 2 * target_direction) - direction_offset)

        try:
            cells = []
            for coordinate in cell_coordinates:
                if coordinate[0]<0 or coordinate[1]<0: # cater for -1 case, which is acceptable by python
                    return False
                cells.append(arena_map.map_cells[int(coordinate[0])][int(coordinate[1])])
            for cell in cells:
                if cell.is_obstacle or not cell.discovered:
                    return False
        except IndexError:
            return False

        return True

    @classmethod
    def next_move(cls, robot, arena_map):
        if cls.look(Direction.RIGHT, robot, arena_map):
            robot.rotate(90)
            if cls.look(Direction.UP, robot, arena_map):
                robot.move_forward()
        elif cls.look(Direction.UP, robot, arena_map):
            robot.move_forward()
        elif cls.look(Direction.LEFT, robot, arena_map):
            robot.rotate(-90)
            if cls.look(Direction.UP, robot, arena_map):
                robot.move_forward()
        else:
            robot.rotate(90)
            robot.rotate(90)

