# -*- coding:utf-8 -*-
import socket
import time
import threading
import Monitor

local_ip = socket.gethostbyname(socket.getfqdn(socket.gethostname()))


class Peer:
    def __init__(self, id, ip, port):
        self.id = id
        self.ip = ip
        self.port = port
        self.timer = 0
        self.state = False


class Server:
    def __init__(self):
        self.address = (local_ip, 40000)
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.serverSocket.settimeout(0.5)
        self.clients = []

    def bind_address(self):
        self.serverSocket.bind(self.address)

    def generate_client_message(self):
        clients_msg = ''
        for item in self.clients:
            clients_msg = clients_msg + item.id + 'a' + item.ip + 'b' \
                          + str(item.port) + 'c' + str(int(item.state)) + 'N'
        clients_msg = clients_msg + "E" + str(len(self.clients))  # E是结束标识符，之后信息是注册表中有几个客户信息
        return clients_msg

    def check_state(self):
        while True:
            for item in self.clients:
                if time.time()-item.timer >= 30:
                    item.state = False
                    # print("{}已下线".format(item.id))
            time.sleep(5)

    def get_client_message(self, monitor):
        while True:
            try:
                data, ip_port = self.serverSocket.recvfrom(1024)  # 接收来自客户端的信息
                data = data.decode('utf-8')
                if data:
                    print(data)
                    register_flag = False  # 若该客户端第一次注册，值为False
                    temp_id = data[0:data.index('a')]
                    temp_ip = data[data.index('a') + 1: data.index('b')]
                    temp_port = int(data[data.index('b')+1:])
                    for item in self.clients:
                        if temp_id == item.id:  # 若该客户端已注册过，只将其状态设为True
                            item.state = True
                            item.ip = temp_ip
                            item.port = temp_port
                            item.timer = time.time()
                            register_flag = True
                    if not register_flag:  # 若客户端第一次注册，将该客户端添加到self.clients中
                        temp_peer = Peer(temp_id, temp_ip, temp_port)
                        temp_peer.state = True
                        temp_peer.timer = time.time()
                        self.clients.append(temp_peer)
                    clients_message = self.generate_client_message()
                    print(clients_message)
                    self.serverSocket.sendto(clients_message.encode('utf-8'), ip_port)
                    print("{}注册成功".format(temp_id))
            except socket.timeout:
                pass
            monitor.update_peers(self.clients)
            time.sleep(3)


if __name__ == '__main__':
    server = Server()
    server.bind_address()
    app = Monitor.Monitor()
    threads = []
    thread = threading.Thread(target=server.get_client_message, args=(app,))
    threads.append(thread)
    thread = threading.Thread(target=server.check_state)
    threads.append(thread)
    for t in threads:
        t.start()
    app.run()
    for t in threads:
        t.join()
