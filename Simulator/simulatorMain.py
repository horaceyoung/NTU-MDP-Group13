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
exploration_instance = exploration.Exploration(300, 20, player_robot, arena_map, True, comm)

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
                comm.send_mapdescriptor(descriptor[0],descriptor[1])
            if event.key == pg.K_d:
                pass

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
    if sensor_val != 0:
        exploration_instance.exploration_loop()
    robot_group.draw(screen)
    # map update
    arena_map.map_update()
    pg.display.update()
    pg.time.delay(3000)
