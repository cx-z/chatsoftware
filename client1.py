# -*- coding:utf-8 -*-
import socket,time
from multiprocessing import *

serveraddress = ('127.0.0.1', 40000)#服务器IP地址和端口号
#获取本机ip
myname = socket.getfqdn(socket.gethostname(  ))
myip = socket.gethostbyname(myname)
client1address = (myip,40001)  #本机IP地址和端口号

statelist = [0, 0, 0]   #客户端状态

class client:
    def __init__(self,name, ipaddress,port):
        self.name = "client1"
        self.ipaddress = "127.0.0.1"
        self.port = 40001

client1 = client('client1', "127.0.0.1", 40001)
client2 = client('client2', "127.0.0.1", 40002)
client3 = client('client3', "127.0.0.1", 40003)
clients = [client1, client2, client3]   #客户端集合

def register():

    message = "1" + str(40001)  #客户端1，端口号为40001
    message = message.encode("utf-8")
    connectserver.send(message)
    print("注册成功")
    #connectserver.close()

def get_client_information():  #从服务器获取其他客户端IP地址和端口号

    try:
        recv_data = connectserver.recv(1024)
        recv_data = recv_data.decode("utf-8")
        if len(recv_data) != 0:
            for i in range(len(clients)):
                statelist[i] = int(recv_data[recv_data.index(str(i)+'a')+2])   #客户端是否在线
                clients[i].ipaddress = recv_data[recv_data.index(str(i)+'b')+2 : recv_data.index(str(i)+'c')]   #客户端的IP地址
                clients[i].port = int(recv_data[recv_data.index(str(i)+'c')+2 : recv_data.index(str(i)+'d')])   #客户端的端口号
                print(clients[i].port)
    except socket.timeout:
        pass



if __name__ == '__main__':

    connectserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # 一个socket连接服务器
    connectserver.connect(serveraddress)
    connectserver.settimeout(2)

    connectclient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #另一个socket绑定端口监听其他客户端
    connectclient.bind(client1address)
    connectclient.listen(2)

    lasttimer = time.time() #上次注册时间戳
    while True:
        time.sleep(1)
        timer = time.time()
        if (timer-lasttimer)>=3:
            print("准备注册")
            register()

            lasttimer = timer
            print("1")
        else:
            #print("上次注册的时间戳为" + str(lasttimer))
            pass

        get_client_information()