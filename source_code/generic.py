import socket
import os
import json
import time

PYTHON_COMMAND = "python"


'''
* To check if current_port is being used by other process
* In case of blocked port, method return True
'''
def is_blocked(port):
    try:
        sct = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sct.bind(("localhost", port))
        sct.close()
        return False
    except Exception as err:
        return True

'''
* Return list of ports available for #number of Nodes available
'''
def get_ports(curr_port, size):
    ports = []

    while len(ports) < size:
        if not is_blocked(curr_port):
            ports.append(curr_port)
        curr_port += 1
    return ports

'''
* To open each node in different processes where it'll have unique port number assign for communication
'''
def spawn_windows(self_id, port_list):
    os.system(f'start cmd /k {PYTHON_COMMAND} source_code\\node.py {self_id} "{json.dumps(port_list)}"')


if __name__ == "__main__":
    NODE_COUNT = int(input("Enter total numbers of client machine (Nodes): "))

    port_list = []
    curr_port = 8000
    port_list = get_ports(curr_port, NODE_COUNT)

    print("Nodes Created\nExiting...")
    time.sleep(1)

    for i in range(NODE_COUNT):
        spawn_windows(str(i+1), port_list)