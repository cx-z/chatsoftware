# -*- coding:utf-8 -*-
import tkinter
import time
import socket
import queue
import traceback


class Application:
    def __init__(self, client_socket, my_id):
        self.my_id = my_id
        self.c_socket = client_socket  # 初始化时输入聊天对方的ID、地址和套接字
        self.c_name = []  # 聊天人名字
        self.c_address = []  # 聊天人地址
        self.c_num = 0  # 聊天人数量

        self.current_id = -1  # 当前聊天界面的联系人
        self.sendSeq = []  # 最近发送给联系人的消息的序列号
        self.recvSeq = []  # 最近从联系人收到的消息的序列号
        self.sendMsg = []  # 所有发送给联系人但尚未确认的消息
        self.sendCnt = []  # 发送给每个联系人的消息总数

        self.root = tkinter.Tk()
        # 创建frame容器
        self.frmLTs = []
        self.txtMsgLists = []
        for i in range(self.c_num):
            frmLT = tkinter.Frame(width=500, height=320, bg='white')  # 已发送和已接收消息所在的框
            self.frmLTs.append(frmLT)
            txtMsgList = tkinter.Text(frmLT)  # 已发送和已接收的消息
            txtMsgList.tag_config('Green', foreground='#008C00')  # 创建tag
            self.txtMsgLists.append(txtMsgList)
        self.frmLC = tkinter.Frame(width=500, height=150, bg='white')
        self.frmLB = tkinter.Frame(width=500, height=30)
        self.frmRT = tkinter.Frame(width=200, height=500)
        # 创建控件
        self.txtMsg = tkinter.Text(self.frmLC)
        self.txtMsg.bind("<KeyPress-Up>", self.send_message_event)
        self.btnSend = tkinter.Button(self.frmLB, text='发送', width=8, command=self.send_message)
        self.btnCancel = tkinter.Button(self.frmLB, text='取消', width=8, command=self.cancel_message)
        # 联系人按钮
        self.btn_clients = []
        for item in self.c_name:
            temp_btn = tkinter.Button(self.frmRT, text=item, width=30)
            temp_btn.bind('<Button-1>', self.btn_click)
            self.btn_clients.append(temp_btn)

    def create_app(self):  # 在聊天框架中画出各部件
        self.root.title(self.my_id)
        # 窗口布局
        for i in range(self.c_num):
            if i == 0:  # 初始界面显示和第一个联系人的对话
                self.frmLTs[i].grid(row=0, column=0, columnspan=2, padx=1, pady=3)
                self.frmLTs[i].grid_propagate(0)
                self.txtMsgLists[i].grid()
            else:  # 初始界面和其他联系人的聊天界面隐藏
                self.frmLTs[i].grid_forget()
                self.txtMsgLists[i].grid_forget()
        self.frmLC.grid(row=1, column=0, columnspan=2, padx=1, pady=3)
        self.frmLB.grid(row=2, column=0, columnspan=2)
        self.frmRT.grid(row=0, column=2, rowspan=3, padx=2, pady=3)
        # 固定大小
        self.frmLC.grid_propagate(0)
        self.frmLB.grid_propagate(0)
        self.frmRT.grid_propagate(0)
        self.btnSend.grid(row=2, column=0)
        self.btnCancel.grid(row=2, column=1)
        self.txtMsg.grid()
        # 联系人按钮
        for btn in self.btn_clients:
            btn.grid(row=self.btn_clients.index(btn))

    def add_linkman(self, c_name, address):  # 在聊天界面右侧添加新的联系人
        self.c_name.append(c_name)
        self.c_address.append(address)

        self.sendSeq.append(-1)  # 添加发送给该联系人的消息的序列号初始值
        self.recvSeq.append(-1)  # 添加从该联系人收到的消息的序列号初始值

        frmLT = tkinter.Frame(width=500, height=320, bg='white')  # 已发送和已接收消息所在的框
        self.frmLTs.append(frmLT)
        txtMsgList = tkinter.Text(frmLT)  # 已发送和已接收的消息
        txtMsgList.tag_config('Green', foreground='#008C00')  # 创建tag
        self.txtMsgLists.append(txtMsgList)
        temp_btn = tkinter.Button(self.frmRT, text=c_name, width=30)
        temp_btn.bind('<Button-1>', self.btn_click)
        self.btn_clients.append(temp_btn)
        temp_btn.grid(row=self.btn_clients.index(temp_btn))
        self.c_num += 1
        self.recvSeq.append(-1)
        self.sendSeq.append(-1)
        self.sendCnt.append(0)
        self.sendMsg.append(queue.Queue())

    def del_linkman(self, c_name):  # 删除不在线的联系人
        temp_id = self.c_name.index(c_name)
        self.btn_clients[temp_id].destroy()
        self.frmLTs[temp_id].destroy()
        self.txtMsgLists[temp_id].destroy()
        del self.btn_clients[temp_id]
        del self.c_address[temp_id]
        del self.c_name[temp_id]
        del self.frmLTs[temp_id]
        del self.txtMsgLists[temp_id]
        del self.recvSeq[temp_id]
        del self.sendSeq[temp_id]
        del self.sendCnt[temp_id]
        del self.sendMsg[temp_id]
        self.c_num = self.c_num - 1
        if not self.c_num:
            self.root.title(self.my_id)
        if self.c_num == 0:
            self.current_id = -1

    def btn_click(self, event=None):  # 点击各联系人对应的按钮，切换聊天界面
        btn_text = event.widget['text']
        for i in range(self.c_num):
            if btn_text == self.c_name[i]:
                self.current_id = i
                self.root.title('{}与{}聊天'.format(self.my_id, self.c_name[self.current_id]))
                self.frmLTs[i].grid(row=0, column=0, columnspan=2, padx=1, pady=3)
                self.frmLTs[i].grid_propagate(0)
                self.txtMsgLists[i].grid()
            else:
                self.frmLTs[i].grid_forget()
                self.txtMsgLists[i].grid_forget()

    def notify(self, c_id):
        data = 'E'
        data += str(self.recvSeq[c_id])
        self.c_socket.sendto(data.encode('utf-8'), self.c_address[c_id])

    def reSend(self, c_id):  # 重新发送未被对方收到的消息
        size = self.sendMsg[c_id].qsize()
        for i in range(size):
            msg = self.sendMsg[c_id].get()
            try:
                self.c_socket.sendto(msg.encode('utf-8'), self.c_address[self.current_id])
            except socket.timeout:
                continue
            except (KeyboardInterrupt, SystemExit):
                raise
            except:
                traceback.print_exc()
            self.sendMsg[c_id].put(msg)

    def send_message(self):  # 将消息发送给当前聊天窗口对应的联系人
        s_msg = 'N' + str(self.sendCnt[self.current_id]) + 'T'
        s_msg += self.txtMsg.get('0.0', tkinter.END) + ' '
        s_msg += str(self.recvSeq[self.current_id])
        self.sendMsg[self.current_id].put(s_msg)
        if self.current_id != -1:
            try:
                print(self.current_id)
                self.c_socket.sendto(s_msg.encode('utf-8'), self.c_address[self.current_id])
                str_msg = "我:" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n'
                self.txtMsgLists[self.current_id].insert(tkinter.END, str_msg, 'Green')
                self.txtMsgLists[self.current_id].insert(tkinter.END, self.txtMsg.get('0.0', tkinter.END))
                self.txtMsg.delete('0.0', tkinter.END)
            except socket.error:
                self.txtMsgLists[self.current_id].insert(tkinter.END, "对方不在线", 'Green')
        else:
            pass

    def send_message_event(self, event):  # Up键作为发送消息的快捷键
        if event.keysym == 'Up':
            self.send_message()

    def cancel_message(self):  # 取消已写到待发送窗口的信息
        self.txtMsg.delete('0.0', tkinter.END)

    def delOldMsg(self, c_id, newLastSendSeq):
        for i in range(newLastSendSeq-self.sendSeq[c_id]):
            self.sendMsg[c_id].get()
        self.sendSeq[c_id] = newLastSendSeq

    def findblank(self, msg):  # 查找最后一个空格
        for i in range(len(msg)):
            if msg[-1 - i] == ' ':
                return -1 - i
        return len(msg)

    def receive_message(self):  # 从socket处接收信息，并根据发送地址将信息写到对应联系人的聊天窗口
        while True:
            if self.current_id != -1:
                try:
                    r_msg, ip_port = self.c_socket.recvfrom(1024)
                    r_msg = r_msg.decode('utf-8')
                    c_id = self.c_address.index(ip_port)
                    if r_msg[0] == 'E':
                        newLastSendSeq = int(r_msg[1:])
                        self.delOldMsg(c_id)
                        self.reSend(c_id)
                        continue
                    elif r_msg[0] == 'N':
                        #print()
                        cur_recv_seq = int(r_msg[1:r_msg.index('T')])
                        tempidx = self.findblank(r_msg)
                        newLastSendSeq = int(r_msg[tempidx+1:])
                        self.delOldMsg(c_id, newLastSendSeq)
                        if cur_recv_seq - self.recvSeq[c_id] != 1:
                            self.notify(c_id)
                            continue
                        str_msg = self.c_name[c_id] + '：' \
                            + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n'
                        self.txtMsgLists[c_id].insert(tkinter.END, str_msg, 'Green')
                        self.txtMsgLists[c_id].insert(tkinter.END, r_msg[r_msg.index('T')+1:tempidx])
                except socket.timeout:
                    pass
                except socket.error:
                    self.txtMsgLists[c_id].insert(tkinter.END, "对方不在线!", 'Green')
            else:
                pass

    def run(self):
        self.root.mainloop()
