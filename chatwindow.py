# -*- coding:utf-8 -*-
from tkinter import *

import time,socket,threading

class chatwindow:

    def __init__(self,client):
        # 创建窗口 
        self.t = Tk()
        self.client = client
        self.t.title('与' +  self.client +'聊天中')

        #接收到其他客户端的消息
        #self.message = clientsocket.recv(1024)
        self.message = str(time.ctime())

        # 创建frame容器
        self.frmLT = Frame(width=500, height=320, bg='white')
        self.frmLC = Frame(width=500, height=150, bg='white')
        self.frmLB = Frame(width=500, height=30)
        self.frmRT = Frame(width=200, height=500)

        # 创建控件
        self.txtMsgList = Text(self.frmLT)
        self.txtMsgList.tag_config('greencolor', foreground='#008C00')  # 创建tag
        self.txtMsg = Text(self.frmLC)   #发送的消息
        self.txtMsg.bind(self.sendMsgEvent)
        self.btnSend = Button(self.frmLB, text='发 送', width=8, command=self.sendMsg)   #发送消息的按键
        self.btnCancel = Button(self.frmLB, text='取消', width=8, command=self.cancelMsg)

        # 窗口布局
        self.frmLT.grid(row=0, column=0, columnspan=2, padx=1, pady=3)
        self.frmLC.grid(row=1, column=0, columnspan=2, padx=1, pady=3)
        self.frmLB.grid(row=2, column=0, columnspan=2)
        self.frmRT.grid(row=0, column=2, rowspan=3, padx=2, pady=3)
        # 固定大小
        self.frmLT.grid_propagate(0)
        self.frmLC.grid_propagate(0)
        self.frmLB.grid_propagate(0)
        self.frmRT.grid_propagate(0)

        self.btnSend.grid(row=2, column=0)
        self.btnCancel.grid(row=2, column=1)
        # lblImage.grid()
        self.txtMsgList.grid()
        self.txtMsg.grid()

        self.gm = threading.Thread(target=self.getMsg)
        self.gm.setDaemon(True)
        self.gm.start()

    def sendMsg(self):#发送消息
        self.strMsg = '我:' + time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()) +'\n '
        self.txtMsgList.insert(END, self.strMsg, 'greencolor')
        self.txtMsgList.insert(END, self.txtMsg.get('0.0', END))
        self.txtMsg.delete('0.0', END)

    def cancelMsg(self):#取消消息
        self.txtMsg.delete('0.0', END)

    def sendMsgEvent(self, event): #发送消息事件
        if event.keysym == "Up":
            self.sendMsg()

    def getMsg(self): #接收消息
        while True:
            time.sleep(5)
            if len(self.message) != 0:
                self.strMsg = self.client + '：' + time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()) + '\n '
                self.txtMsgList.insert(END, self.strMsg, 'greencolor')
                self.txtMsgList.insert(END,self.message+'\n')
                self.message = str(time.ctime())

    def getMsgEvent(self,event): #接收消息事件
        while True:
            if len(self.message) != 0 or event.keysym == "Up":
                self.getMsg()

    def runwindow(self):
        self.t.mainloop()


if __name__ == '__main__':
    chatwin = chatwindow("client1")
    chatwin.runwindow()