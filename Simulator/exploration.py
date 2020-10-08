from configurations import *
from vec2D import swap_coordinates
import time
import commMgr
import pygame as pg



class Exploration:
    def __init__(self,coverage_limit, time_limit, robot, arena_map, realRun, robot_group, screen,comm=None):
        self.robot = robot
        self.map = arena_map
        self.coverage_limit = coverage_limit
        self.time_limit = time_limit
        self.start_time = 0
        self.end_time = 0
        self.area_explored = 0
        self.realRun = realRun
        self.comm = comm
        self.counter = 0  # counter for calibration. when robot move 5 times, need to calibrate again
        #######Need to ask whether is move 5 times then calibrate or move 5 times forward then calibrate###########
        self.robot_group = robot_group
        self.screen = screen
        self.check = 0

    def initialize_exploration(self):
        print("Starting Exploration...")
        self.comm.send_ready()
        self.start_time = time.time()
        self.end_time = self.start_time + self.time_limit

    def exploration_loop(self):

        if not self.realRun:
            self.next_move(self.robot, self.map)
            print(
                "Robot current position x,y: ",
                self.robot.location[0],
                self.robot.location[1],
            )
        # (Added) Real Run ############################################
        else:
            self.nextRealMove(self.robot, self.map, self.comm)
            print("next real move executed")

        self.area_explored = self.calculate_area_explored()
        print("Area Explored: " + str(self.area_explored))

    # Check if the direction relative to the robot has free space -
    def look(self, direction, robot, arena_map):
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

        cell_coordinates = list()  # cells to be looked
        cell_coordinates.append(pg.Vector2(robot.location + 2 * target_direction))
        cell_coordinates.append(
            pg.Vector2(robot.location + 2 * target_direction) + direction_offset
        )
        cell_coordinates.append(
            pg.Vector2(robot.location + 2 * target_direction) - direction_offset
        )

        try:
            cells = []
            for coordinate in cell_coordinates:
                if (
                    coordinate[0] < 0 or coordinate[1] < 0
                ):  # cater for -1 case, which is acceptable by python
                    return False
                cells.append(
                    arena_map.map_cells[int(coordinate[0])][int(coordinate[1])]
                )
            for cell in cells:
                if cell.is_obstacle:
                    return False
        except IndexError:
            print("!!!! Index Error !!!!")
            return False

        return True


    def next_move(self, robot, arena_map):

        if self.look(Direction.RIGHT, robot, arena_map):
            robot.rotate(90)
            # if self.look(Direction.UP, robot, arena_map):
            #     robot.move_forward()
        elif self.look(Direction.UP, robot, arena_map):
            robot.move_forward()
        elif self.look(Direction.LEFT, robot, arena_map):
            robot.rotate(-90)
        else:
            robot.rotate(90)
            robot.rotate(90)

    def nextRealMove(self, robot, arena_map, comm):
        if self.look(Direction.RIGHT, robot, arena_map):
            if(self.check == 1):
                if self.look(Direction.UP, robot, arena_map):
                    print("check for nextRealMove after turning right:",self.check)
                    robot.move_forward()
                    comm.send_movement_forward()
                    self.check = 0
            else:
                print("check for nextRealMove before turning right:",self.check)
                robot.rotate(90)
                comm.send_movement_rotate_right()
                self.check = 1
            # if self.look(Direction.UP, robot, arena_map):
            #     robot.move_forward()
        elif self.look(Direction.UP, robot, arena_map):
            robot.move_forward()
            comm.send_movement_forward()
            self.check = 0
        elif self.look(Direction.LEFT, robot, arena_map):
            if(self.check == 1):
                if self.look(Direction.UP, robot, arena_map):
                    robot.move_forward()
                    comm.send_movement_forward()
                    self.check = 0
                    print("check for nextRealMove after turning left:",self.check)
                else:
                    robot.rotate(-90)
                    comm.send_movement_rotate_left()
                    self.check = 1
                    print("check for nextRealMove before turning left:",self.check)
            else:
                robot.rotate(-90)
                comm.send_movement_rotate_left()
                self.check = 1
                print("check for nextRealMove before turning left:",self.check)
        else:
            robot.rotate(90)
            robot.rotate(90)
            comm.send_movement_rotate_back()
            self.check = 1


    def calculate_area_explored(self):
        explored_arena_count = 0
        for cell_row in self.map.map_cells:
            for cell in cell_row:
                if cell.discovered:
                    explored_arena_count += 1
        return explored_arena_count

    # def sense(self):
    #     sensor_val = self.robot.real_sense(self.map,self.comm)
    #     self.map.map_update()
    #     pg.display.update()
    #     self.map.cells_group.draw(self.screen)
    #     if sensor_val != 0:
    #         self.exploration_loop()
    #     self.robot_group.draw(self.screen)
    #     # map update
    #     self.map.map_update()
    #     pg.display.update()
    #     pg.time.delay(3000)

    """
    def canCalibrateOnTheSpot(botDir):
        #row get robot current row position
        #col get robot current col position
        row = bot.getRobotPosRow()
        col = bot.getRobotPosCol()

        #Check whether can calibrate using front sensor
        if(botDir == Direction.UP):
            return exploredMap.getIsObstacleOrWall(row + 2, col - 1) && exploredMap.getIsObstacleOrWall(row + 2, col) && exploredMap.getIsObstacleOrWall(row + 2, col + 1)
        elif(botDir == Direction.RIGHT):
            return exploredMap.getIsObstacleOrWall(row + 1, col + 2) && exploredMap.getIsObstacleOrWall(row, col + 2) && exploredMap.getIsObstacleOrWall(row - 1, col + 2)
        elif(botDir == Direction.DOWN):
            return exploredMap.getIsObstacleOrWall(row - 2, col - 1) && exploredMap.getIsObstacleOrWall(row - 2, col) && exploredMap.getIsObstacleOrWall(row - 2, col + 1)
        elif(botDir == Direction.LEFT):
            return exploredMap.getIsObstacleOrWall(row + 1, col - 2) && exploredMap.getIsObstacleOrWall(row, col - 2) && exploredMap.getIsObstacleOrWall(row - 1, col - 2)

        #Check whether can calibrate using right sensor
        if(botDir == Direction.UP):
            return exploredMap.getIsObstacleOrWall(row + 1, col + 2)
        elif(botDir == Direction.RIGHT):
            return exploredMap.getIsObstacleOrWall(row - 2, col + 1)
        elif(botDir == Direction.DOWN):
            return exploredMap.getIsObstacleOrWall(row - 1, col - 2)
        elif(botDir == Direction.LEFT):
            return exploredMap.getIsObstacleOrWall(row + 2, col - 1)

        return False



    def getCalibrationDirection(self,origDir):


        dirToCheck = getNextDir(origDir)                  #right
        if (canCalibrateOnTheSpot(dirToCheck)):
            return dirToCheck

        dirToCheck = getPrevDir(origDir)               #left turn
        if (canCalibrateOnTheSpot(dirToCheck)):
            return dirToCheck

        dirToCheck = getPrevDir(dirToCheck)           #u turn
        if (canCalibrateOnTheSpot(dirToCheck)):
            return dirToCheck

        return None




    def calibrateBot(self):
        origDir = bot.getRobotCurDir()
        if(self.canCalibrateOnTheSpot(origDir)):
            comm.send_movement(Movement.CALIBRATE)
        else:
            targetDir = self.getCalibrationDirection(origDir)
            turnCounter = getTurn(origDir,targetDir)
            if(turnCounter == 1):
                self.robot.rotate(90)
                self.comm.send_movement(Movement.RIGHT.value,False)
            elif(turnCounter == -1)
                self.robot.rotate(-90)
                self.comm.send_movement(Movement.LEFT.value,False)
            else:
                self.robot.rotate(90)
                self.robot.rotate(90)
                self.comm.send_movement(Movement.RIGHT.value,False)
                self.comm.send_movement(Movement.RIGHT.value,False)
            comm.send_movement(Movement.CALIBRATE)
    """


if __name__ == "__main__":
    print(DIRECTION_VALUE[Direction.UP])
