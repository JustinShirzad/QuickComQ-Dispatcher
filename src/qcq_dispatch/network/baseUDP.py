""" BaseSocket.py
This is the fundamental creation of socket.
This stores all the important, highly reusable functions of a socket

Author : Emma
Notes / Comments
This is the modified from the previous BaseUDP.py.
"""

import socket
import sys
import time
import random
import os 
import ast
#enum
import enum
from enum import auto

# Log
import logging
log = logging.getLogger()
log.setLevel(logging.DEBUG)


class SocketType(enum.IntEnum):
    SOCK_BROADCAST_UDP = auto()
    SOCK_UDP = auto()
    SOCK_MULTICAST_UDP = auto()

class BaseSocket():
    
    def __init__(self,type:SocketType,ip:str=None, port:int=0,binding:bool=False):
        """BaseSocket - the basics of socket

        Args:
            type (SocketType): SocketType Enum
            ip (str, optional): This Device IP. Defaults to None (get from system).
            port (int, optional): Port of Socket. Defaults to 0(randomised).
            binding (bool, optional): Binds the socket to a specific port for reusability. Defaults to False.
        """
        self.ip:str = ip
        self.port:int = port
        self.type = type
        self.sock:socket = self._init_sock(type)
        self.is_ready = self._bind_sock() if binding is True else True

    @property 
    def ip(self):
        return self._ip

    @ip.setter
    def ip (self,value):
        if value is None: # since not specified , using system's IP
            value = self._obtain_sys_ip()
        if not isinstance(value, str): # type validation
            raise TypeError(f"Need IP Address (v4) in string formmat, received {type(value)}")
        self._ip = value

    @property 
    def port(self):
        return self._port
    
    @port.setter
    def port(self,value:int):
        if not isinstance(value,int): # type validation
            raise TypeError(f"We need an Integer value not {type(value)=}")
        if value == 0: #use generated port
            self._port = self._generate_port()
            self.use_generated_port = True 
        elif 1024 < value < 65535:  # do not edit this !!!
            self._port = value
            self.use_generated_port = False    
        else:
            raise ValueError("Port must be in range 1024 ~ 65535")
        
    @property
    def addr(self):
        """Returns:
            tuple: ip address + port
        """
        return (self.ip,self.port)
    
    def __str__(self):
        return f"{self.addr}"
    
    def __repr__(self):
        return f"{self.__class__.__name__} created on {self.addr}, available = {self.is_ready}"
    
    def close(self):
        """closes the socket"""
        self.is_ready = False
    
    def _bind_sock(self) -> bool:
        """
        Binds the socket to it's ip and a port
        """
        is_binded = False
        tries = 0
        max_tries = 3
        
        while not is_binded and tries < max_tries + 1:
            try:
                self.sock.bind(self.addr)
                is_binded = True
            except socket.error as se:
                is_binded = False
                log.debug(f"socket binding fail {se}")
                if self.use_generated_port is True: 
                    # generates port and tries again
                    self.port = self._generate_port()
                continue                    
        if is_binded is False:
            raise ConnectionError("Socket was not Activated Correctly")    
        return is_binded
        
    @staticmethod
    def _init_sock(type:SocketType) -> socket.socket:
        """ Initialise socket
        Initailise socket for broadcasting in UDP
        Args:
            type(SocketType):an Enum from SocketType
        Returns:
            socket.socket: returns the initailised socket
        """
        if type == SocketType.SOCK_BROADCAST_UDP:
            broadcast = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            broadcast.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            broadcast.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            return broadcast
        elif type == SocketType.SOCK_UDP: 
            udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            return udp
        elif type == SocketType.SOCK_MULTICAST_UDP:
            multicast = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            multicast.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            multicast.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            return multicast            
        
    @staticmethod
    def _obtain_sys_ip() -> str:
        """
        Obtaining system's ip address *This may not work in Arch linux
        Params:
            os_system(sys.platform) =  current os_system.
        Raises:
            ValueError: No matching os system, cannot obtain IP, will need to input manually.
        Returns:
            ip (str): system's ip address
        """
        os_system = sys.platform
        match os_system:
            case 'win32':
                ip = socket.gethostbyname(socket.gethostname())
            case 'linux':
                ip = os.popen('hostname -I').read().strip().split(" ")[1]
                print(f'available : {os.popen("hostname -I").read().strip().split(" ")} , using : {ip}')
            case 'darwin':
                ip = os.popen('ipconfig getifaddr en0').read().strip()
            case _:
                raise ValueError("Cannot Obtain IP, Please input ip address manually")       
        return ip
    
    @staticmethod
    def _generate_port() -> int:
        port = random.randint(5000, 9000)
        log.debug(f"port generated : {port}")
        return port

    
    @staticmethod
    def is_valid_port(port: int) -> bool:
        return 1024 < port < 65535
    
    @staticmethod
    def string_to_tuple(ip_with_port_string:str) -> tuple :
        return ast.literal_eval(ip_with_port_string)

    
if __name__ == "__main__":
    test_sock = BaseSocket(type=SocketType.SOCK_UDP,binding=True)
    print(repr(test_sock))