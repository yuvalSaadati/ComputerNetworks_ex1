import socket
import sys
import time


def start_connection(server_port, parent_ip, parent_port, txt_file):
    # load domains data from file to dictionary
    dic = {} # domain_name:line
    data_txt = open(txt_file, 'r')
    while True:
        line = data_txt.readline()
        if not line:
            data_txt.close()
            break
        if line == "\n":
            continue
        line_list = line.split(",")
        dic[line_list[0]] = line

    # add \n just in case there isn't
    with open(txt_file, "a") as data_txt:
        data_txt.write("\n")

    # create socket with port 'server_port'
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('', int(server_port)))

    while True:
        # receive from client domain_name and addr=(ip,port) of client
        domain_name, addr = s.recvfrom(1024)
        decoded_domain_name = domain_name.decode()
        if decoded_domain_name in dic.keys():
            # check if the data is dynamic
            if dic[decoded_domain_name].count(",") == 3:
                # we reach here only if we have a parent.
                # calculating TTL
                line_list = dic[decoded_domain_name].split(",")
                learning_time, ttl = float(line_list[3]), int(line_list[2])
                if learning_time + ttl > time.time():
                    # we can return the current data to the client
                    s.sendto((line_list[0] + "," + line_list[1] + "," + line_list[2] + "\n").encode(), addr)
                else:
                    # ask the data from the father server
                    data_parent = connect_to_parent(domain_name, parent_ip, parent_port, s)
                    insert_data_to_dic(domain_name, data_parent, dic)
                    write_data_to_file(txt_file, dic[decoded_domain_name])
                    # send domain data to client
                    s.sendto(data_parent, addr)
            else:
                # data that was in the file from the beginning.
                # send the data to the client.
                s.sendto(dic[decoded_domain_name].encode(), addr)
        else:
            # we reach here only if we have a parent.
            # server calls to his parent server.
            data_parent = connect_to_parent(domain_name, parent_ip, parent_port, s)
            insert_data_to_dic(domain_name, data_parent, dic)
            write_data_to_file(txt_file, dic[decoded_domain_name])
            # send domain data to client
            s.sendto(data_parent, addr)


# Get the data from the parent server
def connect_to_parent(domain_name, ip, port, soket,):
    soket.sendto(domain_name, (ip, int(port)))
    data_parent, addr_parent = soket.recvfrom(1024)
    return data_parent


def insert_data_to_dic(domain_name, data_parent, dic):
    decoded_domain_name = domain_name.decode()
    decoded_data_parent = data_parent.decode()
    temp_data_parent = decoded_data_parent.strip('\n')
    # save the new data in dic with the time it was taken.
    dic[decoded_domain_name] = temp_data_parent + "," + time.time().__str__() + "\n"


def write_data_to_file(txt_file, data):
    with open(txt_file, "a") as data_txt:
        data_txt.write(data)


if __name__ == '__main__':
    start_connection(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
