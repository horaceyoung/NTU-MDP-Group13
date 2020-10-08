import time
import fastest_path
import exploration
import map
import robot
import commMgr

from configurations import *

pg.init()
screen = pg.display.set_mode((1024, 768))
pg.display.set_caption("MDP Arena Simulator")

# Initializations
clock = pg.time.Clock()
player_robot = robot.Robot()
robot_group = pg.sprite.Group(player_robot)
arena_map = map.Map()
arena_map.generate_map("map_config_0.txt")
realRun = False

# exploration_instance.initialize_exploration()
# an unresolved issue

running = True
comm = commMgr.TcpClient("192.168.13.13", 4413)
#comm = commMgr.TcpClient("127.0.0.1", 22)
comm.run()
counter = 0
exploration_instance = exploration.Exploration(300, 400, player_robot, arena_map, True, robot_group, screen,comm)
#status = "NIL"
#check = 0
#started = 0

while running:
    # controls
    for event in pg.event.get():
        if event.type == pg.QUIT:
            comm.disconnect()
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_w:
                fastest_path.astar(arena_map, (18, 1), (1, 13))
            if event.key == pg.K_e:
                # exploration_instance = exploration.Exploration(298, 100, player_robot, arena_map, False)
                exploration_instance.initialize_exploration()
            if event.key == pg.K_h:
                fastest_path.astar(arena_map, player_robot.location, (18, 1))
                player_robot.rotateBackDefault()
            if event.key == pg.K_UP:
                comm.send_movement_forward()
            if event.key == pg.K_LEFT:
                comm.send_movement_rotate_left()
            if event.key == pg.K_RIGHT:
                comm.send_movement_rotate_right()
            if event.key == pg.K_DOWN:
                comm.update_queue()
            if event.key == pg.K_p:
                comm.take_picture()
            if event.key == pg.K_c:
                player_robot.real_sense(arena_map,comm)
            if event.key == pg.K_a: #Test for getting android command
                try:
                    print("Android Command Read:",comm.get_android_command())
                except Exception as android:
                    print("Error Reading Android Command:",android)
            if event.key == pg.K_s: #Test for getting sensor value
                try:
                    print("Sensor Value Read:",comm.get_sensor_value())
                except Exception as sense:
                    print("Error Reading Sensor Value:",sense)
            if event.key == pg.K_m:
                descriptor = arena_map.generate_descriptor_strings()
                comm.send_mapdescriptor(descriptor[0],descriptor[1],player_robot.location[1],convertY(player_robot.location[0]),getDirectionValue(player_robot.direction))
            if event.key == pg.K_d:
                pass
    #90:right,180:down,270:left,0:up
    # fastest_path.astar(arena_map,player_robot.location,(18,1))
    screen.fill((0, 0, 0))
    # generate the map
    if counter==0:
        comm.send_ready()
        print("send ready called")
        counter += 1

    sensor_val = player_robot.real_sense(arena_map,comm)
    arena_map.map_update()
    pg.display.update()
    arena_map.cells_group.draw(screen)
    #if exploration_instance.area_explored <= exploration_instance.coverage_limit or (exploration_instance.area_explored>=10 and player_robot.location != (18,1)):
    '''
    if(check == 0):
        comm.update_queue()
        status = comm.get_android_command()
        check = 1
        if(status == "ES"):
            exploration_instance.exploration_loop()
            started = 1
    if exploration_instance.area_explored < exploration_instance.coverage_limit or exploration_instance.start_time < exploration_instance.end_time or not started:
        exploration_instance.exploration_loop()
    '''
    if exploration_instance.area_explored < exploration_instance.coverage_limit or exploration_instance.start_time < exploration_instance.end_time:
        print("exploration loop function in simulatorMain runs")
        exploration_instance.exploration_loop()
    else:
        #started = 0
        fastest_path.astar(arena_map, player_robot.location, 18, 1, comm)
        player_robot.rotateBackDefault()
    robot_group.draw(screen)
    # map update
    arena_map.map_update()
    #descriptor = arena_map.generate_descriptor_strings()
    #comm.send_mapdescriptor(descriptor[0],descriptor[1],player_robot.location[1],player_robot.location[0],getDirectionValue(player_robot.direction))
    pg.display.update()
    pg.time.delay(1300)
