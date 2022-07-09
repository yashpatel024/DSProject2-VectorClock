import os
import time
import json
import threading
from sys import argv
from sockets import send_request, increament_clock, create_server, internal_process


def sender(clock_val, self_id, port_list):
    while True:
        node_input = input().strip()

        if node_input in ["e", "exit"]:
            break

        # Not valid values
        # Not numeric, not int, out of range

        invalid_flag = False
        if node_input.isnumeric():
            send_id = int(node_input, 10)
            if send_id <= len(port_list):
                print(f"Before: {clock_val}")
                if send_id == self_id:
                    increament_clock(clock_val, self_id)
                    internal_process(self_id)
                else:
                    send_request(self_id, port_list[send_id-1], increament_clock(clock_val, self_id))
                print(f"After: {clock_val}\n")
            else:
                invalid_flag = True
        else:
            invalid_flag = True

        if invalid_flag:
            print("Invalid value. Please Enter correct value. :)")

    print("Finished")


def receiver():
    time.sleep(int(argv[1]))


if __name__ == "__main__":
    self_id = int(argv[1])
    port_list = json.loads(argv[2])
    node_count = len(port_list)

    os.system(f"title Node-{self_id} \tPort-{port_list[self_id-1]}")

    clock_val = [0]*node_count

    t1 = threading.Thread(target=create_server, args=[self_id, port_list[self_id-1], clock_val])
    t1.start()

    sender(clock_val, self_id, port_list)
    input()