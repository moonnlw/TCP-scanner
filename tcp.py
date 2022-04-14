import argparse
import socket
from threading import Thread, Lock
from queue import Queue
import sys

N_THREADS = 2000

q = Queue()
print_lock = Lock()


def tcp_port_scan(port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)

        result = s.connect_ex((host, port))
        if result == 0:
            print("Port {} is open".format(port))
        s.close()

    except socket.gaierror:
        print("\n Wrong hostname")
        sys.exit()
    except socket.error:
        print("\n Host does not answer")
        sys.exit()


def scan_thread():
    global q
    while True:
        port = q.get()
        tcp_port_scan(port)
        q.task_done()


def main(host, ports):
    global q
    for t in range(N_THREADS):
        t = Thread(target=scan_thread)
        t.daemon = True
        t.start()
    for port in ports:
        q.put(port)
    q.join()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="port scanner")
    parser.add_argument("host")
    parser.add_argument("--ports", "-p", dest="port_range", default="1-65535")
    args = parser.parse_args()
    host, port_range = args.host, args.port_range
    start_port, end_port = port_range.split("-")
    start_port, end_port = int(start_port), int(end_port)
    ports = [p for p in range(start_port, end_port)]
    main(host, ports)
