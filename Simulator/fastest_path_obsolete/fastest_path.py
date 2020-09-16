import configurations


#Node class for A* path finding
class Node:

    #initialize a node
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    #to compare if 2 nodes are equal by comparing their positions
    def __eq__(self, other):
        return self.position == other.position


#A* path finding algorithm
def astar(maze, start, end):

    #Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f - 0

    #Initialize both open and closed list
    open_list = []
    closed_list = []

    #Add the start node
    open_list.append(start_node)

    #Loop until end is reached
    while open_list:

        #Get the node with the smallest f
        current_node = open_list[0]
        current_index = 0
        for index,item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        #Pop current node off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        #If the goal is reached
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent

            #Return reversed path
            return path[::-1]


        #Generate children
        children = []
        for new_position in [(0,-1),(0,1),(-1,0),(1,0)]:

            #Get children node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            #Ensure the position is within the maze
            if node_position[0] > configurations.MAP_ROWS-1 or node_position[0] < 0 or node_position[1] > configurations.MAP_COLS-1 or node_position[1] < 0:  ############## Made Changes Here
                continue

            #Ensure the new position is not an obstacle
            if (maze.getCell(node_position[0],node_position[1]).getIsObstacle() != 0 or maze.getCell(node_position[0],node_position[1]).isExplored == False): ################ Made Changes Here
                continue

            #Create new node
            new_node = Node(current_node, node_position)

            #Append to children list
            children.append(new_node)


        #Loop through children
        for child in children:

            #If child is already visited (on closed list), do nothing
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            #Initialize the f, g, and h values
            child.g = current_node.g + 1
            #Add penalty if requires turning
            if current_node != start_node:
                if not ((child.position[0] == current_node.position[0] and child.position[0] == current_node.parent.position[0]) or (child.position[1] == current_node.position[1] and child.position[1] == current_node.parent.position[1])):
                    child.g += 3
            #Robot can only turn 90 degrees
            #Manhattan distance as heuristic
            child.h = abs(child.position[0] - end_node.position[0]) + abs(child.position[1] - end_node.position[1])
            child.f = child.g + child.h

            existed = False
            #Child is already in open_list and child is further from source than it is initially, do not append it to open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    existed = True
                    break

            #Add the child to the open list
            if not existed:
                open_list.append(child)


# Added New Stuff #####################
def runAStar(path,maze):
    for cell in path:
        maze.getCell(cell[0],cell[1]).isPath = True
    printPathMap(maze)

# Added New Stuff ######################
def printPathMap(maze):
    print_row = ""
    printList = []
    for x in range(configurations.MAP_ROWS):
        for y in range(configurations.MAP_COLS):
            #string = str(test_map.grid[x][y].row) + " "
            if(maze.inStartZone(x,y) or maze.inGoalZone(x,y)):
                string = "1 "
            elif(maze.getCell(x,y).isPath):
                string = "8 "
            else:
                string = "0 "
            print_row = print_row + string
        printList.append(print_row)
        print_row = ""

    for i in range(len(printList)):
        print(printList[i])
    #print(print_row)
    #    print_row = ""

def main():

    maze = [[0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
            [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0],
            [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    start = (0,0)
    end = (14,19)

    path = astar(maze, start, end)
    for cell in path:
        maze[cell[0]][cell[1]] = 8
    for line in maze:
        print(line)

if __name__ == '__main__':
    main()
