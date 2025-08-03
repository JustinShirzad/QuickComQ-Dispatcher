""" SENDER
Sender includes :
    1. Sender            - UDP socket for server.
    2. Broadcaster       - UDP broadcast socket for server.
    3. Multicaster       - UDP Multicast socket (Not Implemented)
Raises:
    NotImplementedError: if user try to use an empty function
"""
import ast
import logging

from qcq_dispatch.network.robotCommand import RobotCommand
from qcq_dispatch.network.baseUDP import BaseSocket
import yaml
try:
    from yaml import CLoader as Loader
except ImportError as e:
    from yaml import Loader

import socket
          
class YamlSender():
    def __init__(self):
        # addr = "src/TeamControl/utils/ipconfig.yaml"
        addr = "src/qcq_dispatch/ipconfig.yaml"
        file = open(addr, "r")
        self.robot = yaml.load(file, Loader)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send_command(self, command: RobotCommand):
        if not isinstance(command, RobotCommand):
            raise TypeError("only RobotCommand Object Allowed")
        
        robot_id = str(command.robot_id)
        destination = self.robot[robot_id]["ip"]
        port = self.robot[robot_id]["port"]
        print(f"[YAMLSender] : sending to robot :{robot_id} : {command} @ ({destination}, {port})")
        encoded_command: bytes = command.encode()
        self.sock.sendto(encoded_command, (destination, port))

if __name__ == "__main__":
    s = YamlSender()
    # Test with individual commands
    cmd1 = RobotCommand(robot_id=1, vx=1.0, vy=0.0, w=0.0, kick=0, dribble=0)
    cmd2 = RobotCommand(robot_id=2, vx=0.0, vy=1.0, w=0.0, kick=0, dribble=0)
    
    s.send_command(cmd1)
    s.send_command(cmd2)