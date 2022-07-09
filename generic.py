import socket
import os
import signal
import json
import time

import multiprocessing


NODE_COUNT = 3
PYTHON_COMMAND = "python"

n = 0


def is_blocked(port):
    try:
        sct = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sct.bind(("localhost", port))
        sct.close()
        return False
    except Exception as err:
        return True


def get_ports(curr_port, size):
    ports = []

    while len(ports) < size:
        if not is_blocked(curr_port):
            ports.append(curr_port)
        curr_port += 1
    return ports


def spawn_windows(self_id, port_list):
    os.system(f'start cmd /k {PYTHON_COMMAND} node.py {self_id} "{json.dumps(port_list)}"')

# TODO: Remove


ports_to_block = [8001, 8002, 8008]
blocked_connections = []


def block_ports():
    for port in ports_to_block:
        sct = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sct.bind(("localhost", port))
        # sct.listen(10)
        blocked_connections.append(sct)
        print("1")


def unblock_blocked():
    for con in blocked_connections:
        con.close()

# TODO: Remove


block_ports()
port_list = []
curr_port = 8000

NODE_COUNT = int(input("Enter total numbers of client machine: "))

port_list = get_ports(curr_port, NODE_COUNT)

for i in range(NODE_COUNT):
    spawn_windows(str(i+1), port_list)

print("Nodes Created...\nExiting !!!")
time.sleep(2)
unblock_blocked()
