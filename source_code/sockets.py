from socket import socket, AF_INET, SOCK_STREAM
import json

# Localhost IP
IP = "127.0.0.1"

'''
* Help command
'''
def print_help(total_client):
    width = 60
    print()
    print("~"*width)
    print(f"{'HELP':^{width}}")
    print("~"*width)
    print(
        "# To get help anytime enter \"help\"\n"
        "# Message Format: [{TO_CLIENT_ID} {MESSAGE_TO_SEND}]\n"
        f"# Possible range of values of TO_CLIENT_ID: [1-{total_client}]"
    )
    print("~"*width, end="\n\n")


'''
* When Node calls for internal process
'''
def internal_process(self_id, message):
    print(f"Internal process completed of {self_id} with message:")
    print(message)


'''
* Increament of Vector clock for node specific id
'''
def increament_clock(clock_val, id):
    clock_val[id-1] += 1
    return clock_val


'''
* Comparing sender and receiver clock while communication to assign new Vector_Clock to receiver
'''
def compare_clock(self_clock, sender_clock):
    for i in range(len(self_clock)):
        self_clock[i] = max(self_clock[i], sender_clock[i])
    return self_clock


'''
* Listener for node
'''
def create_server(self_id, port_list, clock_val):
    with socket(AF_INET, SOCK_STREAM) as sock:
        sock.bind((IP, port_list[self_id-1]))
        sock.listen(10)
        print(f"[+] Listening at: {(IP, port_list[self_id-1])}")
        print_help(len(port_list))
        while True:
            conn, addr = sock.accept()
            req = json.loads(conn.recv(65536))
            print(f"Message received from Node {req.get('sender_id')}:")
            print(req.get("message", ""))

            print(f"Before = {clock_val}")
            increament_clock(clock_val, self_id)

            print(f"After = {compare_clock(clock_val, req.get('sender_clock'))} \n")
            conn.send(json.dumps({"a": "success"}).encode())
            conn.close()


'''
* Send message from one node to other
'''
def send_request(sender_id, port, clock_val, message):
    json_data = {
        "sender_clock": clock_val,
        "sender_id": sender_id,
        "message": message
    }
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect((IP, port))
    sock.send(json.dumps(json_data).encode())
    response = json.loads(sock.recv(65536))
    sock.close()


if __name__ == "__main__":
    print_help(5)