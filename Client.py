# -*- coding:utf-8 -*-
import socket
import time


class Peer:
    def __init__(self, id, ip, port, state):
        self.id = id
        self.ip = ip
        self.port = port
        self.timer = 0
        self.state = state


class Client:
    def __init__(self, id, port1, port2):
        self.id = id
        self.ip = socket.gethostbyname(socket.getfqdn(socket.gethostname()))
        self.port1 = port1  # port1与服务器通信
        self.port2 = port2  # port2与其他客户端通信
        self.peers = []
        self.toServer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.toClient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def bind_address(self):
        self.toServer.bind((self.ip, self.port1))
        self.toClient.bind((self.ip, self.port2))

    def register(self):
        register_msg = str(self.id) + 'a' + self.ip + 'b' + str(self.port2)
        last_timer = time.time()
        server_addr = ('169.254.57.250', 40000)
        while True:
            if (time.time()-last_timer) >= 5:
                self.toServer.sendto(register_msg.encode('utf-8'), server_addr)
                print('注册成功')
                last_timer = time.time()

    def get_client_info(self):
        while True:
            info, addr = self.toServer.recvfrom(1024)
            info = info.decode('utf-8')
            print(len(self.peers))
            if info:
                for i in range(int(info[info.index('E')+1:])):
                    record_flag = False  # 该客户信息不在本机注册表self.peers中，则为False
                    temp_id = info[0:info.index('a')]
                    temp_ip = info[info.index('a')+1:info.index('b')]
                    temp_port = int(info[info.index('b')+1:info.index('c')])
                    temp_state = bool(int(info[info.index('c')+1:info.index('N')]))
                    for item in self.peers:
                        if item.id == temp_id:  # 若该客户信息已在本机注册表中，只修改其信息
                            item.ip = temp_ip
                            item.port = temp_port
                            item.state = temp_state
                            record_flag = True
                    if not record_flag:  # 将未记录的客户信息加入到注册表中
                        temp_peer = Peer(temp_id, temp_ip, temp_port, temp_state)
                        self.peers.append(temp_peer)
                    info = info[info.index('N')+1:]
