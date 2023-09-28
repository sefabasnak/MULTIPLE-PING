import socket
import struct
import argparse
import time
import threading

ICMP_ECHO_REQUEST = 8

def calculate_checksum(packet):
    checksum = 0
    for i in range(0, len(packet), 2):
        checksum += (packet[i] << 8) + packet[i + 1]
    checksum = (checksum >> 16) + (checksum & 0xFFFF)
    return ~checksum & 0xFFFF

def send_ping_request(dest_ip):
    icmp_checksum = 0
    icmp_id = 1  
    icmp_seq = 1

    icmp_header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, icmp_checksum, icmp_id, icmp_seq)
    data = b"abcdefghijklmnopqrstuvwabcdefghi"


    icmp_checksum = calculate_checksum(icmp_header + data)
    icmp_header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, socket.htons(icmp_checksum), icmp_id, icmp_seq)

    try:
        
        raw_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        raw_socket.sendto(icmp_header + data, (dest_ip, 0))
        
        # ICMP yanıtını al
        recv_packet, addr = raw_socket.recvfrom(1024)
        round_trip_time = (time.time() - start_time) * 1000
        return round_trip_time, addr[0]
    except socket.timeout:
        return None, None

def ping_host(host, timeout):
    global start_time
    start_time = time.time()
    try:
        dest_ip = socket.gethostbyname(host)
        while not stop_event.is_set():
            response_time, dns_ip = send_ping_request(dest_ip)
            if response_time is not None:
                if dns_ip:
                    print(f"{host} ({dns_ip}) Ping successfully sent to the address. Ping time: {response_time} ms")
                else:
                    print(f"{host} Ping successfully sent to the address. Ping time: {response_time} ms")
            else:
                print(f"{host} An error occurred while pinging the address.")
            time.sleep(1)
    except Exception as e:
        print(f"{host} An error occurred while pinging the address: {str(e)}")

def ping_hosts_from_file(file_path, timeout):
    try:
        with open(file_path, "r") as file:
            targets = file.read().splitlines()
    except FileNotFoundError:
        print(f"{file_path} File not found.")
        return
    except Exception as e:
        print(f"An error occurred while opening the file: {str(e)}")
        return

    for target in targets:
        ping_thread = threading.Thread(target=ping_host, args=(target, timeout))
        ping_thread.start()

def main():
    global stop_event
    stop_event = threading.Event()

    parser = argparse.ArgumentParser(description="Tool used for ICMP ping to IP addresses.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-u", "--url", help="Pings an IP or domain address", type=str)
    group.add_argument("-l", "--list", help="Pings IP or domain addresses from a file", type=str)
    parser.add_argument("-t", "--timeout", help="Maximum timeout for ping responses (seconds)", type=float, default=2)
    try:
        args = parser.parse_args()
    except KeyboardInterrupt:
        stop_event.set()
        return

    if args.url:
        ping_host(args.url, args.timeout)

    if args.list:
        ping_hosts_from_file(args.list, args.timeout)

    try:
        while not stop_event.is_set():
            pass
    except KeyboardInterrupt:
        stop_event.set()

if __name__ == "__main__":
    main()