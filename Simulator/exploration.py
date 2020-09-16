from configurations import *
from vec2D import swap_coordinates
import time

class Exploration:
    def __init__(self, coverage_limit,time_limit, robot, arena_map):
        self.robot = robot
        self.map = arena_map
        self.coverage_limit = coverage_limit
        self.time_limit = time_limit
        self.start_time = 0
        self.end_time = 0
        self.area_explored = 0

    def initialize_exploration(self):
        print("Starting Exploration...")
        self.start_time = time.time()
        self.end_time = self.start_time + self.time_limit
        self.exploration_loop()

    def exploration_loop(self):
        self.next_move(self.robot, self.map)
        self.area_explored = self.calculate_area_explored()
        print("Area Explored: " + str(self.area_explored))

    #Check if the direction relative to the robot has free space -
    @classmethod
    def look(cls, direction, robot, arena_map):
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


    def calculate_area_explored(self):
        explored_arena_count = 0
        for cell_row in self.map.map_cells:
            for cell in cell_row:
                if cell.discovered:
                    explored_arena_count += 1
        return explored_arena_count