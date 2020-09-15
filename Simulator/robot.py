import numpy
import configurations
import map
from settings import *

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
        pg.sprite.Sprite.__init__(self)

        self.image = robot_image
        self.direction = pg.math.Vector2(0, -1)
        self.velocity = 35

        self.spawn_point = 17 * map.Map.cell_length

        self.rect = self.image.get_rect()
        self.rect.x = map.Map.cell_gap
        self.rect.y = self.spawn_point + map.Map.cell_gap #position of the robot
        self.center = pg.math.Vector2(self.rect.x+50, self.rect.y+50)

        self.censors = pg.sprite.Group()
        self.add_censor(20, 40, 0, -50)
        self.add_censor(20, 40, 40, -50)
        self.add_censor(20, 40, -40, -50)

    def add_censor(self, width, height, center_x_offset, center_y_offset):
        self.censors.add(Censor(width, height, center_x_offset, center_y_offset, self))

    def is_in_arena(self, rect):
        if rect.x>= map.Map.arena_border_left and rect.x <= map.Map.arena_border_right and rect.y >= map.Map.arena_border_up and rect.y <= map.Map.arena_border_down:
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

    def rotate(self, degree):
        self.image  = pg.transform.rotate(self.image, -degree)
        self.direction = self.direction.rotate(degree).normalize()

        #update censors
        for censor in self.censors:
            censor.rotation_update(self, degree)



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

    def collision_update(self, map):
        collided_cells = pg.sprite.spritecollide(self, map.cells_group, False)
        collided_cells_with_distance = []
        for collided_cell in collided_cells:
            collided_cells_with_distance.append((collided_cell, pg.math.Vector2(self.rect.x, self.rect.y).distance_to(
                pg.math.Vector2(collided_cell.rect.x, collided_cell.rect.y))))

        #sort the cells by the distance between its center and the center of the censor
        collided_cells_with_distance.sort(key=lambda x:x[1])
        for collided_cell_tuple in collided_cells_with_distance:
            map.map_cells[collided_cell_tuple[0].row][collided_cell_tuple[0].col].discovered = True
            if collided_cell_tuple[0].is_obstacle:
                collided_cell_tuple[0].update_color((0, 0, 255))
                break



