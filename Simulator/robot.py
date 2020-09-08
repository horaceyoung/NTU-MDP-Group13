from settings import *
import pygame as pg
import map_generator as mapp
import numpy
import map
import configurations
import sensor
import exploration

"""
Robot Sensor placement
           ^   ^   ^
          SR  SR  SR
        << SR
         [X] [X] [X]
    < LR [X] [X] [X] SR >
         [X] [X] [X]

"""

class Robot(pg.sprite.Sprite):
    def __init__(self):
        # For Map Simulator
        pg.sprite.Sprite.__init__(self)

        self.image = robot_image
        self.direction = pg.math.Vector2(0, -1)
        self.velocity = 35

        self.spawn_point = 17 * mapp.Map.tile_length

        self.rect = self.image.get_rect()
        self.rect.x = mapp.Map.tile_gap
        self.rect.y = self.spawn_point + mapp.Map.tile_gap #position of the robot
        self.center = pg.math.Vector2(self.rect.x+50, self.rect.y+50)

        self.censors = pg.sprite.Group()
        self.add_censor(20, 40, 0, -50)
        self.add_censor(20, 40, 40, -50)
        #self.explorer = explorer
        # For Testing purposes
        #self.explorer.runExploration()
        #self.realMap.setAllUnexplored()
        self.add_censor(20, 160, -20, -50)


    def add_censor(self, width, height, center_x_offset, center_y_offset):
        self.censors.add(Censor(width, height, center_x_offset, center_y_offset, self))

    def is_in_arena(self, rect):
        if rect.x>= mapp.Map.arena_border_left and rect.x <= mapp.Map.arena_border_right and rect.y >= mapp.Map.arena_border_up and rect.y <= mapp.Map.arena_border_down:
            return True
        else:
            return False

    def move_forward(self):
        # if the robot is within the arena
        _rect = pg.Rect(self.rect)
        _rect.x += self.direction[0] * self.velocity
        _rect.y += self.direction[1] * self.velocity

        if self.is_in_arena(_rect):
            self.rect.x += self.direction[0] * self.velocity
            self.rect.y += self.direction[1] * self.velocity
            # update center
            self.rect.center = pg.math.Vector2(self.rect.x+50, self.rect.y+50)
            for censor in self.censors:
                censor.position_update(self)



        # For testing purposes
        #self.test_robot.move(configurations.Movement.FORWARD)
        #self.test_robot.setSensors()
        #self.test_robot.sense(self.exploredMap,self.realMap)
        #self.debugVirtualMap()
        #self.testRobotPositionUpdate(configurations.Movement.FORWARD)



    def rotate(self, degree):
        self.image  = pg.transform.rotate(self.image, -degree)
        self.direction = self.direction.rotate(degree).normalize()

        #update censors
        for censor in self.censors:
            censor.rotation_update(self, degree)

        # For testing purposes
        if(degree == 90):
            dir = configurations.Movement.RIGHT
        elif(degree == -90):
            dir = configurations.Movement.LEFT
        #self.test_robot.move(dir)
        #self.test_robot.setSensors()
        #self.test_robot.sense(self.exploredMap,self.realMap)
        #self.testRobotPositionUpdate(dir)

    # This is only for TESTING & DEBUGGING PURPOSES
    def debugVirtualMap(self):
        test_row = ""
        for x in range(configurations.MAP_ROWS):
            for y in range(configurations.MAP_COLS):
                #string = str(test_map.grid[x][y].row) + " "
                if(self.exploredMap.grid[x][y].isExplored):
                    string = "1 "
                else:
                    string = "0 "
                test_row = test_row + string
            print(test_row)
            test_row = ""

    # This is only for TESTING & DEBUGGING PURPOSES
    """
    def testRobotPositionUpdate(self,dir):
        self.test_robot.move(dir)
        x = self.test_robot.posRow
        y = self.test_robot.posCol
        print("Current Position: "+ str(x) +" , "+ str(y))
        self.exploredMap.grid[x][y].setIsExplored(True)
        self.debugVirtualMap()
    """
    # This is only for TESTING & DEBUGGING PURPOSES
    #def testSensorPositionUpdate(self):



class Censor(pg.sprite.Sprite):
    def __init__(self, width, height, center_x_offset, center_y_offset, robot):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((width, height), pg.SRCALPHA, 32)
        self.rect = self.image.get_rect()
        self.rect.center = robot.rect.center + pg.math.Vector2(center_x_offset, center_y_offset)
        self.color = (255, 0, 0)

        pg.draw.rect(self.image, self.color, pg.Rect(0, 0, width, height), 4)

    def rotation_update(self, robot, degree):
        center_diff_vec = pg.math.Vector2(tuple(numpy.subtract(self.rect.center, robot.rect.center)))
        rotated_center_diff_vec = center_diff_vec.rotate(degree)
        self.rect.center = robot.rect.center + rotated_center_diff_vec
        self.image = pg.transform.rotate(self.image, degree)



    def position_update(self, robot):
        self.rect.center += robot.velocity * robot.direction



class RobotAlgo:
    def __init__(self,row,col,realBot,player_robot):
        self.posRow = row
        self.posCol = col
        self.robotDir = configurations.START_DIR
        self.speed = configurations.SPEED
        self.realBot = realBot
        self.touchedGoal = False

        self.srFrontLeft = sensor.Sensor(configurations.SENSOR_SHORT_RANGE_L, configurations.SENSOR_SHORT_RANGE_H, self.posRow + 1, self.posCol - 1, self.robotDir, "SRFL")
        self.srFrontCenter = sensor.Sensor(configurations.SENSOR_SHORT_RANGE_L, configurations.SENSOR_SHORT_RANGE_H, self.posRow + 1, self.posCol, self.robotDir, "SRFC")
        self.srFrontRight = sensor.Sensor(configurations.SENSOR_SHORT_RANGE_L, configurations.SENSOR_SHORT_RANGE_H, self.posRow + 1, self.posCol + 1, self.robotDir, "SRFR")
        self.srLeft = sensor.Sensor(configurations.SENSOR_SHORT_RANGE_L, configurations.SENSOR_SHORT_RANGE_H, self.posRow + 1, self.posCol - 1, self.findNewDirection(configurations.Movement.LEFT), "SRL")
        self.srRight = sensor.Sensor(configurations.SENSOR_SHORT_RANGE_L, configurations.SENSOR_SHORT_RANGE_H, self.posRow + 1, self.posCol + 1, self.findNewDirection(configurations.Movement.RIGHT), "SRR")
        self.lrLeft = sensor.Sensor(configurations.SENSOR_LONG_RANGE_L, configurations.SENSOR_LONG_RANGE_H, self.posRow, self.posCol - 1, self.findNewDirection(configurations.Movement.LEFT), "LRL")

        self.player_robot = player_robot


    # Set current robot position, void
    def setRobotPos(self, row, col):
        self.posRow = row
        self.posCol = col

    # Set robot direction, void
    def setRobotDir(self,dir):
        self.robotDir = dir

    # Set robot speed/delay between movements, void
    def setSpeed(self,speed):
        self.speed = speed

    # update if robot touched the goal
    def updateTouchedGoal(self):
        if(self.posRow == configurations.GOAL_ROW and self.posCol == configurations.GOAL_COL):
            self.touchedGoal = True
    """
    def turnLeft(self):
        Robot.rotate(-90)

    def turnRight(self):
        Robot.rotate(90)

    def turnBack(self):
        Robot.rotate(180)
    """
    # MIGHT NEED TO ADD IN MOVEMENT LATER TO UPDATE MAP. NOW ONLY DEBUG STAGE
    def move(self, m):
        if(m == configurations.Movement.FORWARD):
            if(self.robotDir == configurations.Direction.NORTH):
                self.posRow += 1
            elif(self.robotDir == configurations.Direction.EAST):
                self.posCol += 1
            elif(self.robotDir == configurations.Direction.SOUTH):
                self.posRow -= 1
            elif(self.robotDir == configurations.Direction.WEST):
                self.posCol -= 1
            self.player_robot.move_forward()
        elif(m == configurations.Movement.BACKWARD):
            if(self.robotDir == configurations.Direction.NORTH):
                self.posRow -= 1
            elif(self.robotDir == configurations.Direction.EAST):
                self.posCol -= 1
            elif(self.robotDir == configurations.Direction.SOUTH):
                self.posRow += 1
            elif(self.robotDir == configurations.Direction.WEST):
                self.posCol += 1
            self.player_robot.rotate(90)
            self.player_robot.rotate(90)
            self.player_robot.move_forward()
        elif(m == configurations.Movement.RIGHT or m == configurations.Movement.LEFT):
            self.robotDir = self.findNewDirection(m)
            if(m == configurations.Movement.RIGHT):
                self.player_robot.rotate(90)
            else:
                self.player_robot.rotate(-90)

        print("Direction: "+ str(self.robotDir.value))

        print("Move: "+ m.value)

        self.updateTouchedGoal()


    def moveForwardMultiple(self,count):
        if(count == 1):
            self.move(configurations.Movement.FORWARD)
        else:
            if(self.robotDir == configurations.Direction.NORTH):
                self.posRow += count
            elif(self.robotDir == configurations.Direction.EAST):
                self.posCol += count
            elif(self.robotDir == configurations.Direction.SOUTH):
                self.posRow += count
            elif(self.robotDir == configurations.Direction.WEST):
                self.posCol += count

    # Everytime need to setSensors when moved
    def setSensors(self):
        if(self.robotDir == configurations.Direction.NORTH):
            self.srFrontLeft.setSensor(self.posRow + 1, self.posCol - 1, self.robotDir)
            self.srFrontCenter.setSensor(self.posRow + 1, self.posCol, self.robotDir)
            self.srFrontRight.setSensor(self.posRow + 1, self.posCol + 1, self.robotDir)
            self.srLeft.setSensor(self.posRow + 1, self.posCol - 1, self.findNewDirection(configurations.Movement.LEFT))
            self.lrLeft.setSensor(self.posRow, self.posCol - 1, self.findNewDirection(configurations.Movement.LEFT))
            self.srRight.setSensor(self.posRow + 1, self.posCol + 1, self.findNewDirection(configurations.Movement.RIGHT))
        elif(self.robotDir == configurations.Direction.EAST):
            self.srFrontLeft.setSensor(self.posRow + 1, self.posCol + 1, self.robotDir)
            self.srFrontCenter.setSensor(self.posRow, self.posCol + 1, self.robotDir)
            self.srFrontRight.setSensor(self.posRow - 1, self.posCol + 1, self.robotDir)
            self.srLeft.setSensor(self.posRow + 1, self.posCol + 1, self.findNewDirection(configurations.Movement.LEFT))
            self.lrLeft.setSensor(self.posRow + 1, self.posCol, self.findNewDirection(configurations.Movement.LEFT))
            self.srRight.setSensor(self.posRow - 1, self.posCol + 1, self.findNewDirection(configurations.Movement.RIGHT))
        elif(self.robotDir == configurations.Direction.SOUTH):
            self.srFrontLeft.setSensor(self.posRow - 1, self.posCol + 1, self.robotDir)
            self.srFrontCenter.setSensor(self.posRow - 1, self.posCol, self.robotDir)
            self.srFrontRight.setSensor(self.posRow - 1, self.posCol - 1, self.robotDir)
            self.srLeft.setSensor(self.posRow - 1, self.posCol + 1, self.findNewDirection(configurations.Movement.LEFT))
            self.lrLeft.setSensor(self.posRow, self.posCol + 1, self.findNewDirection(configurations.Movement.LEFT))
            self.srRight.setSensor(self.posRow - 1, self.posCol - 1, self.findNewDirection(configurations.Movement.RIGHT))
        elif(self.robotDir == configurations.Direction.WEST):
            self.srFrontLeft.setSensor(self.posRow - 1, self.posCol - 1, self.robotDir)
            self.srFrontCenter.setSensor(self.posRow, self.posCol - 1, self.robotDir)
            self.srFrontRight.setSensor(self.posRow + 1, self.posCol - 1, self.robotDir)
            self.srLeft.setSensor(self.posRow - 1, self.posCol - 1, self.findNewDirection(configurations.Movement.LEFT))
            self.lrLeft.setSensor(self.posRow - 1, self.posCol, self.findNewDirection(configurations.Movement.LEFT))
            self.srRight.setSensor(self.posRow + 1, self.posCol - 1, self.findNewDirection(configurations.Movement.RIGHT))

    def findNewDirection(self,m):
        if(m == configurations.Movement.RIGHT):
            return configurations.getNextDir(self.robotDir)
        else:
            return configurations.getPrevDir(self.robotDir)

    # int array of sensor value
    def sense(self,explorationMap,realMap):
        result = []

        result.append(self.srFrontLeft.sense(explorationMap, realMap))
        result.append(self.srFrontCenter.sense(explorationMap, realMap))
        result.append(self.srFrontRight.sense(explorationMap, realMap))
        result.append(self.srLeft.sense(explorationMap, realMap))
        result.append(self.srRight.sense(explorationMap, realMap))
        result.append(self.lrLeft.sense(explorationMap, realMap))

        return result
