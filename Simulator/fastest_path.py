from operator import attrgetter
import pygame as pg
#A* path finding algorithm
def astar(arena_map, start, end):

    # Create start and end node
    start_node = arena_map.map_cells[int(start[0])][int(start[1])]
    start_node.g = start_node.h = start_node.f = 0
    end_node = arena_map.map_cells[end[0]][end[1]]
    end_node.g = end_node.h = end_node.f - 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    #Add the start node
    open_list.append(start_node)

    # Loop until end is reached
    while open_list:
    # for i in range(0,1000):
        # Get the node with the smallest f
        current_node = min(open_list,key=attrgetter('f'))
        # print("poped node:", current_node.position)
        # Pop current node off open list, add to closed list
        open_list.remove(current_node)
        closed_list.append(current_node)

        # If the goal is reached
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current)
                current = current.parent

            for node in path:
                for cell_row in arena_map.map_cells:
                    for cell in cell_row:
                        if node.position == cell.position:
                            #Need to ask how to update get robot current position
                            cell.update_color((255,0,0))
                            cell.discovered = False
                            arena_map.cells_group.add(cell)


        #Generate children
        children = []

        for new_position in [(0,-1),(0,1),(-1,0),(1,0)]:
            #Get children node position
            node_position = current_node.position+ pg.Vector2(new_position[0], new_position[1])
            #Ensure the position is within the maze
            try:
                new_node = arena_map.map_cells[int(node_position[0])][int(node_position[1])]
            except IndexError:
                continue

            #Ensure the new position is not an obstacle
            if new_node.is_obstacle:
                continue

            #Ensure the new position's surrounding 8 blocks is free
            surrounding_node_free = True
            position_offsets = \
            [(-1, -1), (-1, 0), (-1, 1), # Top 3 cells
            (0, -1), (0, 1), # Left and right cells
            (1, -1), (1, 0), (1, 1)] # Lower 3 cells
            for position_offset in position_offsets:
                try:
                    surrounding_node_position = node_position + position_offset
                    # print("surrounding node position", surrounding_node_position)
                    if surrounding_node_position[0]<0 or surrounding_node_position[1]<0:
                        surrounding_node_free = False
                    surrounding_node = arena_map.map_cells[int(surrounding_node_position[0])][int(surrounding_node_position[1])]
                    if surrounding_node.is_obstacle:
                        surrounding_node_free = False
                except IndexError:
                    # print("index error")
                    surrounding_node_free = False

            if not surrounding_node_free:
                continue

            #Append to children list
            if new_node not in closed_list:
                new_node.parent = current_node
                children.append(new_node)

        # for child in children:
        #     print("child", child.position, child.parent.position)


        # Loop through children
        for child in children:
            # Initialize the f, g, and h values
            child.g = current_node.g + 1
            # Add penalty if requires turning
            # if current_node != start_node:
            #     if not ((child.position[0] == current_node.position[0] and child.position[0] ==
            #         current_node.parent.position[0]) or (
            #             child.position[1] == current_node.position[1] and child.position[1] ==
            #         current_node.parent.position[1])):
            #         child.g += 3
            # Robot can only turn 90 degrees
            # Manhattan distance as heuristic
            manhattan_distance_vec = child.position - end_node.position
            child.h = abs(manhattan_distance_vec[0]) + abs(manhattan_distance_vec[1])
            child.f = child.g + child.h

            if child.h + child.f < child.g:
                child.g = child.h + child.f

            if child not in open_list:
                open_list.append(child)
