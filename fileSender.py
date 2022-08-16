import time
import sys
import signal
import socket
import numpy 

PORT = 5064 # Random port
SERVER = socket.getaddrinfo(socket.gethostname(), PORT) # The Server address is automatically found by checking the current computer's IP address
ADDR = ("::1", PORT)
API_DELIMINATOR = "-"
disconnect_msg = "DISCONNECT"

graphData = 0
message_str = ""

Sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
Sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, False)


def signal_handler(signal_in, frame):
    print("\nTerminating Sender...")
    sys.exit(0)
  

def main():
    current = 0  
    signal.signal(signal.SIGINT, signal_handler)
    fName = './new_data/instrumentation_512x512.csv'
    try:
        file_obj = open(fName, "rb")
        data = numpy.loadtxt(file_obj, delimiter=",",
                            skiprows=1, max_rows=None, usecols=(0, 1, 12, 13, 14, 15, 16, 18))      ### MAX ROW LIMIT IS MAX NUMBER OF TIME INSTANCES
    except Exception as e:
        print("Couldn't open file because " + str(e))
    
    for s in (data):
        if(s[1]>current):
            current = s[1]
            time.sleep(1)
        message_str = str(s[0]) + API_DELIMINATOR + str(s[1]) + API_DELIMINATOR + str(s[2]) + API_DELIMINATOR + str(s[3]) + API_DELIMINATOR + str(s[4]) + API_DELIMINATOR + str(s[5]) + API_DELIMINATOR + str(s[6]) + API_DELIMINATOR + str(s[7])
        Sock.sendto(message_str.encode('utf-8'), ADDR)
        print(message_str)

    time.sleep(2)
    print("DISCONNECTING")

if __name__ == '__main__':
    main()
