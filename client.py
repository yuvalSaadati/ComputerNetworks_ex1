import socket
import sys
import socket

""" 
#send message to server:
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.sendto(b'Yuval Saadaty 205956634', ('127.0.0.1', 12345))
data, addr = s.recvfrom(1024)
print(str(data), addr)
s.close()

"""

def connect_to_server(ip, port):
    # create socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        # get domain name from user
        input_domain = input()
        # send domain name to server
        s.sendto(input_domain.encode(), (ip, int(port)))
        # example from server : input_domain = www.biu.ac.il
        # example from parent server : input_domain = www.google.co.il

        data, addr = s.recvfrom(1024)
        # receive from server data = domain name, domain ip, server port
        data_list = str(data).split(",")
        print(data_list[1])
    s.close()


if __name__ == '__main__':
    connect_to_server(sys.argv[1], sys.argv[2])
