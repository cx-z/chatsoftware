# -*- coding:utf-8 -*-
import socket,time,select
from threading import Thread

serveraddress = ('127.0.0.1', 40000)
statelist = [0, 0, 0]   #客户端状态


class client:
    def __init__(self,name, ipaddress,port):

        self.name = name
        self.ipaddress = ipaddress
        self.port = port

client1 = client('client1', "127.0.0.1", 40001)
client2 = client('client2', "127.0.0.1", 40002)
client3 = client('client3', "127.0.0.1", 40003)
clients = [client1, client2, client3]   #客户端集合


def get_client_message(clientsocket, ltimer):
    # 在子进程中循环接受客户端发来的信息，直到客户端发送的为空时,结束接收,并断开连接
    print("0")
    timer = time.time()
    while True:
        try:
            recv_data = clientsocket.recv(1024)
            recv_data = recv_data.decode("utf-8")
            #print(recv_data)
            if len(recv_data) == 0:
                break
            else:
                print("消息来源为客户端%s:%s" % (recv_data[0:1], recv_data))

                clientid = int(recv_data[0:1])-1 #根据报文的第一个字符得到客户端编号
                clients[clientid].ipaddress = recv_data[1:recv_data.index('a')]  #记录注册客户端的IP地址和端口号
                #print("客户端IP地址为：")
                #print(clients[clientid].ipaddress)
                clients[clientid].port = int(recv_data[recv_data.index('a')+1 :])
                print("客户端端口号为：")
                print(clients[clientid].port)
                statelist[clientid] = 1 #将发送消息的客户端状态设为1
                ltimer[clientid] = timer #更新该客户端的时间戳

                peerlist = ''
                for i in range(len(statelist)):  #将客户端信息整理成字符串
                    peerlist = peerlist + str(i)+ 'a' + str(statelist[i]) \
                               + str(i) + 'b' + clients[i].ipaddress \
                               + str(i) + 'c' +str(clients[i].port) \
                               + str(i) +'d'

                print(peerlist)
                for i in range(len(statelist)): #将所有客户端信息发送给每个客户端
                    if statelist[i]:
                        clientsocket.send(peerlist.encode("utf-8"))

            for i in range(len(ltimer)):
                if (timer-ltimer[i])>=30:   #若某客户端超过30秒未注册
                    statelist[i] = 0        #将该客户端的状态设为0
        except socket.timeout:
            break
        except:
            break
    #clientsocket.close()

    return ltimer


if __name__ == '__main__':

    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind(serveraddress)
    serverSocket.listen(3)

    lasttimer = [time.time(), time.time(), time.time()]  # 客户端上次注册的时间戳

    inputs = [serverSocket,]
    outputs = []
    while True:
        time.sleep(1)
        try:
            readable, writeable, exceptional = select.select(inputs, outputs, inputs)
            print(readable)
            for r in readable:
                if r is serverSocket:
                    clientSocket, clientInfo = serverSocket.accept()
                    clientSocket.setblocking(False)
                    inputs.append(clientSocket)
                    print("来了一个新连接",clientSocket,clientInfo)
                else:
                    lasttimer = get_client_message(r,lasttimer)
                    #lasttimer = get_client_message(clientSocket,clientInfo,lasttimer)
        except:
            pass
