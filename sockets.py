import math
from sys import argv, exit, stderr
from socket import socket, AF_INET, SOCK_STREAM
from select import select as sel
from pathlib import Path
import json

IP = "127.0.0.1"


def internal_process(self_id):
    print(f"Internal process completed of {self_id}")


def increament_clock(clock_val, id):
    clock_val[id-1] += 1
    return clock_val


def compare_clock(self_clock, sender_clock):
    for i in range(len(self_clock)):
        self_clock[i] = max(self_clock[i], sender_clock[i])
    return self_clock


def create_server(self_id, self_port, clock_val):
    with socket(AF_INET, SOCK_STREAM) as sock:
        sock.bind((IP, self_port))
        sock.listen(10)
        print(f"[+] Listening on localhost at: {(IP, self_port)}")
        while True:
            conn, addr = sock.accept()
            req = json.loads(conn.recv(65536))
            print(f"Received from Node {req.get('sender_id')}")
            print(f"Before = {clock_val}")
            increament_clock(clock_val, self_id)
            print(f"After = {compare_clock(clock_val, req.get('data'))} \n")
            conn.send(json.dumps({"a": "success"}).encode())
            conn.close()


def send_request(sender_id, port, data):
    json_data = {"data": data, "sender_id": sender_id}
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect((IP, port))
    sock.send(json.dumps(json_data).encode())
    response = json.loads(sock.recv(65536))
    sock.close()
