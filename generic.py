import socket
import os
import signal
import json
import time

NODE_COUNT = 3

def find_port(port):
    """Find a port not in ues starting at given port"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        if s.connect_ex(("localhost", port)) == 0:
            return find_port(port=port + 1)
        else:
            return port

def spawn_windows(self_id, port_list):
    os.system(f"start cmd /k py node.py {self_id} \"{json.dumps(port_list)}\"")

port_list = []
curr_port = 8000

for i in range(NODE_COUNT):
    curr_port = find_port(curr_port+1)
    port_list.append(curr_port)

for i in range(NODE_COUNT):
    spawn_windows(str(i+1), port_list)

print("Nodes Created...\nExiting")
time.sleep(2)
# os.system("exit")
# pid = os.getpid()
# os.kill(pid, signal.SIGABRT)
