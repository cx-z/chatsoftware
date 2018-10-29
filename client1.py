# -*- coding:utf-8 -*-
import socket,time,threading
import chatwindow
from multiprocessing import Process

serveraddress = ('127.0.0.1', 40000)#服务器IP地址和端口号
#获取本机ip
myname = socket.getfqdn(socket.gethostname(  ))
myip = socket.gethostbyname(myname)
client1address = (myip,40001)  #本机IP地址和端口号

statelist = [0, 0, 0]   #客户端状态

class Client():
    def __init__(self,name, ipaddress,port):
        self.name = name
        self.ipaddress = ipaddress
        self.port = port
client1 = Client('client1', "127.0.0.1", 40001)
client2 = Client('client2', "127.0.0.1", 40002)
client3 = Client('client3', "127.0.0.1", 40003)
clients = [client1, client2, client3]  # 客户端集合


def register(ltimer, toserver):
    message = "1" + myip + 'a' + str(40001)  # 客户端1，端口号为40001
    message = message.encode("utf-8")
    while True:
        timer = time.time()
        if (timer-ltimer)>=15:
            toserver.send(message)
            print("注册成功")
            ltimer = time.time()
        #connectserver.close()


def get_client_information(toserver):  #从服务器获取其他客户端IP地址和端口号
    while True:
        try:
            recv_data = toserver.recv(1024)
            recv_data = recv_data.decode("utf-8")
            if len(recv_data) != 0:
                for i in range(len(clients)):
                    statelist[i] = int(recv_data[recv_data.index(str(i)+'a')+2])   #客户端是否在线
                    clients[i].ipaddress = recv_data[recv_data.index(str(i)+'b')+2 : recv_data.index(str(i)+'c')]   #客户端的IP地址
                    clients[i].port = int(recv_data[recv_data.index(str(i)+'c')+2 : recv_data.index(str(i)+'d')])   #客户端的端口号
                    print(clients[i].port)
        except socket.timeout:
            pass
        except:
            pass


def chatwithclient(user,myaddress, useraddress):
    try:
        chatwin = chatwindow.chatwindow(user,myaddress, useraddress)
        print("生成窗口对象")
        chatwin.runwindow()
        print("生成窗口成功")
    except:
        pass

def connectwithclient():
    flag = [True, False, False]  # 客户端1是否已经连接其他客户端的标志位
    while True:
        time.sleep(1)
        for i in range(len(clients)):
            if i>=1 and statelist[i]!=0 and flag[i]==False:
                '''connectclient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 另一个socket绑定端口监听其他客户端
                connectclient.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
                connectclient.bind(client1address)
                connectclient.connect((clients[i].ipaddress, clients[i].port))'''
                toaddress = (clients[i].ipaddress,clients[i].port)
                print("连接成功")
                ti = threading.Thread(target=chatwithclient,args=(clients[i].name,client1address,toaddress))
                ti.setDaemon(False)
                ti.start()
                print("窗口生成了吗？")
                flag[i] = True
            elif statelist[i] == 0:
                print(str(i)+':'+str(statelist[i]))
                flag[i] = False

if __name__ == '__main__':

    connectserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # 一个socket连接服务器
    connectserver.connect(serveraddress)
    connectserver.settimeout(2)

    lasttimer = time.time()  # 上次注册时间戳


    threads = []
    t1 = threading.Thread(target=register, args=(lasttimer,connectserver))
    threads.append(t1)
    t2 = threading.Thread(target=get_client_information, args=(connectserver,))
    threads.append(t2)
    t3 = threading.Thread(target=connectwithclient)
    threads.append(t3)

    for t in threads:
        t.setDaemon(False)
        t.start()

