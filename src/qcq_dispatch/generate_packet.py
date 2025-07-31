import random
import time

from qcq_dispatch.network.robotCommand import RobotCommand

def create_input():
    random_id = random.randint(1, 3) # good
    run_time = random.randrange(1, 10) #good
    
    random_vx = random.randint(0,2)

    command = RobotCommand(robot_id=random_id,vx=random_vx) #changed this

    return command,run_time #this creates tuple automatically 

def generate_w_interval(q,x=5):
    while True:
        packet = create_input()
        q.put(packet)
        time.sleep(x)