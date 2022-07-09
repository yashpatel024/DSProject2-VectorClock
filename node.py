import time
import json
import threading
from sys import argv
from sockets import send_request,increament_clock,create_server,internal_process

def sender(clock_val, self_id, port_list):
    while True:
        node_input = input().strip()

        if node_input in ["e", "exit"]:
            break
            
        send_id = int(node_input,10)

        print(f"Before: {clock_val}")
        if send_id == self_id:
            increament_clock(clock_val,self_id)
            internal_process(self_id)
        else:
            send_request(self_id, port_list[send_id-1], increament_clock(clock_val,self_id))
        print(f"After: {clock_val}\n")

    print("Finished")

def receiver():
    time.sleep(int(argv[1]))

if __name__ == "__main__":
    self_id = int(argv[1])
    print(argv[1])
    print(argv[2])
    port_list = json.loads(argv[2])
    node_count = len(port_list)

    clock_val = [0]*node_count

    t1 = threading.Thread(target=create_server, args=[self_id, port_list[self_id-1], clock_val])  
    t1.start()

    sender(clock_val, self_id, port_list)
    input()
