import configurations
import Exploration.sensor as sensor


class RobotAlgo:
    def __init__(self, row, col, realBot, player_robot):
        self.posRow = row
        self.posCol = col
        self.robotDir = configurations.START_DIR
        self.speed = configurations.SPEED
        self.realBot = realBot
        self.touchedGoal = False

        self.srFrontLeft = sensor.Sensor(
            configurations.SENSOR_SHORT_RANGE_L,
            configurations.SENSOR_SHORT_RANGE_H,
            self.posRow + 1,
            self.posCol - 1,
            self.robotDir,
            "SRFL",
        )
        self.srFrontCenter = sensor.Sensor(
            configurations.SENSOR_SHORT_RANGE_L,
            configurations.SENSOR_SHORT_RANGE_H,
            self.posRow + 1,
            self.posCol,
            self.robotDir,
            "SRFC",
        )
        self.srFrontRight = sensor.Sensor(
            configurations.SENSOR_SHORT_RANGE_L,
            configurations.SENSOR_SHORT_RANGE_H,
            self.posRow + 1,
            self.posCol + 1,
            self.robotDir,
            "SRFR",
        )
        self.srLeft = sensor.Sensor(
            configurations.SENSOR_SHORT_RANGE_L,
            configurations.SENSOR_SHORT_RANGE_H,
            self.posRow + 1,
            self.posCol - 1,
            self.findNewDirection(configurations.Movement.LEFT),
            "SRL",
        )
        self.srRight = sensor.Sensor(
            configurations.SENSOR_SHORT_RANGE_L,
            configurations.SENSOR_SHORT_RANGE_H,
            self.posRow + 1,
            self.posCol + 1,
            self.findNewDirection(configurations.Movement.RIGHT),
            "SRR",
        )
        self.lrLeft = sensor.Sensor(
            configurations.SENSOR_LONG_RANGE_L,
            configurations.SENSOR_LONG_RANGE_H,
            self.posRow,
            self.posCol - 1,
            self.findNewDirection(configurations.Movement.LEFT),
            "LRL",
        )

        self.player_robot = player_robot

    # Set current robot position, void
    def setRobotPos(self, row, col):
        self.posRow = row
        self.posCol = col

    # Set robot direction, void
    def setRobotDir(self, dir):
        self.robotDir = dir

    # Set robot speed/delay between movements, void
    def setSpeed(self, speed):
        self.speed = speed

    # update if robot touched the goal
    def updateTouchedGoal(self):
        if (
            self.posRow == configurations.GOAL_ROW
            and self.posCol == configurations.GOAL_COL
        ):
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
        if m == configurations.Movement.FORWARD:
            if self.robotDir == configurations.Direction.NORTH:
                self.posRow += 1
            elif self.robotDir == configurations.Direction.EAST:
                self.posCol += 1
            elif self.robotDir == configurations.Direction.SOUTH:
                self.posRow -= 1
            elif self.robotDir == configurations.Direction.WEST:
                self.posCol -= 1
            self.player_robot.move_forward()
        elif m == configurations.Movement.BACKWARD:
            if self.robotDir == configurations.Direction.NORTH:
                self.posRow -= 1
            elif self.robotDir == configurations.Direction.EAST:
                self.posCol -= 1
            elif self.robotDir == configurations.Direction.SOUTH:
                self.posRow += 1
            elif self.robotDir == configurations.Direction.WEST:
                self.posCol += 1
            self.player_robot.rotate(90)
            self.player_robot.rotate(90)
            self.player_robot.move_forward()
        elif m == configurations.Movement.RIGHT or m == configurations.Movement.LEFT:
            self.robotDir = self.findNewDirection(m)
            if m == configurations.Movement.RIGHT:
                self.player_robot.rotate(90)
            else:
                self.player_robot.rotate(-90)

        print("Direction: " + str(self.robotDir.value))

        print("Move: " + m.value)

        self.updateTouchedGoal()

    def moveForwardMultiple(self, count):
        if count == 1:
            self.move(configurations.Movement.FORWARD)
        else:
            if self.robotDir == configurations.Direction.NORTH:
                self.posRow += count
            elif self.robotDir == configurations.Direction.EAST:
                self.posCol += count
            elif self.robotDir == configurations.Direction.SOUTH:
                self.posRow += count
            elif self.robotDir == configurations.Direction.WEST:
                self.posCol += count

    # Everytime need to setSensors when moved
    def setSensors(self):
        if self.robotDir == configurations.Direction.NORTH:
            self.srFrontLeft.setSensor(self.posRow + 1, self.posCol - 1, self.robotDir)
            self.srFrontCenter.setSensor(self.posRow + 1, self.posCol, self.robotDir)
            self.srFrontRight.setSensor(self.posRow + 1, self.posCol + 1, self.robotDir)
            self.srLeft.setSensor(
                self.posRow + 1,
                self.posCol - 1,
                self.findNewDirection(configurations.Movement.LEFT),
            )
            self.lrLeft.setSensor(
                self.posRow,
                self.posCol - 1,
                self.findNewDirection(configurations.Movement.LEFT),
            )
            self.srRight.setSensor(
                self.posRow + 1,
                self.posCol + 1,
                self.findNewDirection(configurations.Movement.RIGHT),
            )
        elif self.robotDir == configurations.Direction.EAST:
            self.srFrontLeft.setSensor(self.posRow + 1, self.posCol + 1, self.robotDir)
            self.srFrontCenter.setSensor(self.posRow, self.posCol + 1, self.robotDir)
            self.srFrontRight.setSensor(self.posRow - 1, self.posCol + 1, self.robotDir)
            self.srLeft.setSensor(
                self.posRow + 1,
                self.posCol + 1,
                self.findNewDirection(configurations.Movement.LEFT),
            )
            self.lrLeft.setSensor(
                self.posRow + 1,
                self.posCol,
                self.findNewDirection(configurations.Movement.LEFT),
            )
            self.srRight.setSensor(
                self.posRow - 1,
                self.posCol + 1,
                self.findNewDirection(configurations.Movement.RIGHT),
            )
        elif self.robotDir == configurations.Direction.SOUTH:
            self.srFrontLeft.setSensor(self.posRow - 1, self.posCol + 1, self.robotDir)
            self.srFrontCenter.setSensor(self.posRow - 1, self.posCol, self.robotDir)
            self.srFrontRight.setSensor(self.posRow - 1, self.posCol - 1, self.robotDir)
            self.srLeft.setSensor(
                self.posRow - 1,
                self.posCol + 1,
                self.findNewDirection(configurations.Movement.LEFT),
            )
            self.lrLeft.setSensor(
                self.posRow,
                self.posCol + 1,
                self.findNewDirection(configurations.Movement.LEFT),
            )
            self.srRight.setSensor(
                self.posRow - 1,
                self.posCol - 1,
                self.findNewDirection(configurations.Movement.RIGHT),
            )
        elif self.robotDir == configurations.Direction.WEST:
            self.srFrontLeft.setSensor(self.posRow - 1, self.posCol - 1, self.robotDir)
            self.srFrontCenter.setSensor(self.posRow, self.posCol - 1, self.robotDir)
            self.srFrontRight.setSensor(self.posRow + 1, self.posCol - 1, self.robotDir)
            self.srLeft.setSensor(
                self.posRow - 1,
                self.posCol - 1,
                self.findNewDirection(configurations.Movement.LEFT),
            )
            self.lrLeft.setSensor(
                self.posRow - 1,
                self.posCol,
                self.findNewDirection(configurations.Movement.LEFT),
            )
            self.srRight.setSensor(
                self.posRow + 1,
                self.posCol - 1,
                self.findNewDirection(configurations.Movement.RIGHT),
            )

    def findNewDirection(self, m):
        if m == configurations.Movement.RIGHT:
            return configurations.getNextDir(self.robotDir)
        else:
            return configurations.getPrevDir(self.robotDir)

    # int array of sensor value
    def sense(self, explorationMap, realMap):
        result = []

        result.append(self.srFrontLeft.sense(explorationMap, realMap))
        result.append(self.srFrontCenter.sense(explorationMap, realMap))
        result.append(self.srFrontRight.sense(explorationMap, realMap))
        result.append(self.srLeft.sense(explorationMap, realMap))
        result.append(self.srRight.sense(explorationMap, realMap))
        result.append(self.lrLeft.sense(explorationMap, realMap))

        return result
