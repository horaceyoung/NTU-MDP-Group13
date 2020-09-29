from configurations import *
from cell import Cell
import pygame as pg

class Map:
    # static variables
    height = 20
    width = 15
    config = 0

    map_offset_x = 5
    map_offset_y = 5
    non_obstacle_cell_width = 30 # with of the cell
    cell_length = 35  # cell_length - cell_width = the gap between cell gaps, alter here to adjust length
    cell_gap = cell_length - non_obstacle_cell_width
    arena_border_left = 5
    arena_border_up = 5
    arena_border_right = cell_length * 13
    arena_border_down = cell_length * 18

    cells_group = pg.sprite.Group() # the cells sprite group
    map_cells = [] # a 20 * 15  list holding cell objects

    def __init__(self):
        pass

    def generate_map(self, map_config):

        with open(map_config_path + map_config, 'r') as map_config:
            cell_x = self.map_offset_x
            cell_y = self.map_offset_y
            for row in range(1, 21):
                line = map_config.readline()
                cell_row = []
                for col in range (0, 15):
                    if line[col] == '0':
                        cell = Cell(cell_x, cell_y)
                    elif line[col] == '1':
                        cell = Cell(cell_x, cell_y)
                        cell.is_obstacle = True
                    elif line[col] =='2':
                        cell = Cell(cell_x, cell_y)
                        cell.update_color((255, 255, 0))
                        cell.discovered =  True
                        cell.is_start_goal_zone = True
                    cell.row = row-1
                    cell.col = col
                    cell.position = pg.Vector2(cell.row, cell.col)
                    cell_row.append(cell)
                    cell_x += cell.length + cell.gap
                self.map_cells.append(cell_row)
                cell_x = self.map_offset_x
                cell_y = self.map_offset_y + (cell.length + cell.gap) *  row

        for cell in self.map_cells:
            self.cells_group.add(cell)

    def map_update(self):
        for cell_row in self.map_cells:
            for cell in cell_row:
                if cell.is_obstacle == False and cell.discovered ==True and cell.is_start_goal_zone == False:
                    self.cells_group.remove(cell)

    def generate_descriptor_strings(self):
        # part1
        part1_result = "11\n"
        part2_result = ""
        for row in self.map_cells:
            for col in row:
                if col.discovered:
                    part1_result+="1"
                    if col.is_obstacle:
                        part2_result+='1'
                    else:
                        part2_result+="0"
                elif not col.discovered:
                    part1_result+='0'
            part1_result+="\n"
            part2_result+='\n'
        part1_result += "11\n"
        print("Part1 Map Representation: \n" + part1_result)
        print("Part1 Map Representation in hex: " + str(hex(int(part1_result.replace("\n", ""),2))))
        print("Part2 Map Representation: \n" + part2_result)
        print("Part2 Map Representation in hex: " + str(hex(int(part2_result.replace("\n", ""), 2))))




