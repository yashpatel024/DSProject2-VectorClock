import os
import time
import json
import threading
from sys import argv
from sockets import print_help, send_request, increament_clock, create_server, internal_process

'''
* Take input from Node of receiver node_id and message
'''
def sender(clock_val, self_id, port_list):
    while True:
        input_line = input().strip()  # ID Message
        # Split into parts
        inputs = input_line.split(" ", 1)

        id = inputs[0].strip().lower()
        message = inputs[1] if len(inputs) > 1 else ""
        if id in ["e", "exit"]:
            break
        elif id in ["h", "help"]:
            print_help(len(port_list))
            continue

        # Not valid values
        # Not numeric, not int, out of range
        invalid_flag = False
        if id.isnumeric():
            send_id = int(id, 10)
            if send_id <= len(port_list):
                print(f"Before: {clock_val}")
                if send_id == self_id:
                    increament_clock(clock_val, self_id)
                    internal_process(self_id, message)
                else:
                    send_request(self_id, port_list[send_id-1], increament_clock(clock_val, self_id), message)
                print(f"After: {clock_val}\n")
            else:
                invalid_flag = True
        else:
            invalid_flag = True

        if invalid_flag:
            print("Invalid value. Please Enter correct value. :)")

    print("Finished")

if __name__ == "__main__":
    self_id = int(argv[1])
    port_list = json.loads(argv[2])
    node_count = len(port_list)

    # Changing title of each Node's process
    os.system(f"title Node-{self_id} \tPort-{port_list[self_id-1]}")

    # Initializing Vector clock for Node
    clock_val = [0]*node_count

    # Thread for listening on assigned port, which uses create_server function from sockets.py
    t1 = threading.Thread(target=create_server, args=[self_id, port_list, clock_val])
    t1.start()

    sender(clock_val, self_id, port_list)
    input()