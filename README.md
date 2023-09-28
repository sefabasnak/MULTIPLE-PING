# MULTIPLE-PING
This Python application is used to send ICMP pings to multiple IP addresses.

# Usage  
To use this tool, follow the steps below:

Clone the project:
```bash
git clone https://github.com/sefabasnak/multiple-ping.git
```
Use the following commands to send ICMP pings to IP addresses:
```bash
python3 multiple-ping.py -h
usage: multiple-ping.py [-h] (-u URL | -l LIST) [-t TIMEOUT]

options:
  -h, --help            show this help message and exit
  -u URL, --url URL     Pings an IP or domain address
  -l LIST, --list LIST  Pings IP or domain addresses from a file
  -t TIMEOUT, --timeout TIMEOUT Maximum timeout for ping responses (seconds)
```
Sending a ping to a single IP or domain:
```bash
python multiple-ping.py -u <IP or domain>
```
Sending pings to a list of IP addresses or domains:
```bash
python multiple-ping.py -l <file_path>
```
