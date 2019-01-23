# -*- coding:utf-8 -*-
import tkinter
import time
import socket


class Application:
    def __init__(self, client_socket, my_id, client_id, client_address):
        self.my_id = my_id
        self.c_socket = client_socket  # 初始化时输入聊天对方的ID、地址和套接字
        self.c_id = client_id  # 联系人ID列表
        self.c_address = client_address  # 联系人IP地址和端口号列表
        self.c_num = len(client_id)  # 联系人个数
        self.current_id = 0  # 当前聊天界面的联系人
        self.root = tkinter.Tk()
        # 创建frame容器
        self.frmLTs = []
        self.txtMsgLists = []
        for i in range(self.c_num):
            frmLT = tkinter.Frame(width=500, height=320, bg='white')  # 已发送和已接收消息所在的框
            self.frmLTs.append(frmLT)
            txtMsgList = tkinter.Text(frmLT)  # 已发送和已接收的消息
            txtMsgList.tag_config('greencolor', foreground='#008C00')  # 创建tag
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
        for item in self.c_id:
            temp_btn = tkinter.Button(self.frmRT, text=item, width=30)
            temp_btn.bind('<Button-1>', self.btn_click)
            self.btn_clients.append(temp_btn)

    def create_app(self):
        self.root.title('{}与{}聊天'.format(self.my_id, self.c_id[self.current_id]))
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
        # for i in range(self.c_num):
        #     self.frmLTs[i].grid_propagate(0)
        #     self.txtMsgLists[i].grid()
        self.frmLC.grid_propagate(0)
        self.frmLB.grid_propagate(0)
        self.frmRT.grid_propagate(0)
        self.btnSend.grid(row=2, column=0)
        self.btnCancel.grid(row=2, column=1)
        self.txtMsg.grid()
        # 联系人按钮
        for btn in self.btn_clients:
            btn.grid(row=self.btn_clients.index(btn))

    def btn_click(self, event=None):
        btn_text = event.widget['text']
        for i in range(self.c_num):
            if btn_text == self.c_id[i]:
                self.current_id = i
                self.root.title('{}与{}聊天'.format(self.my_id, self.c_id[self.current_id]))
                self.frmLTs[i].grid(row=0, column=0, columnspan=2, padx=1, pady=3)
                self.frmLTs[i].grid_propagate(0)
                self.txtMsgLists[i].grid()
            else:
                self.frmLTs[i].grid_forget()
                self.txtMsgLists[i].grid_forget()

    def send_message(self):
        s_msg = self.txtMsg.get('0.0', tkinter.END).encode('utf-8')
        try:
            print(self.current_id)
            self.c_socket.sendto(s_msg, self.c_address[self.current_id])
            str_msg = "我:" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n'
            self.txtMsgLists[self.current_id].insert(tkinter.END, str_msg, 'greencolor')
            self.txtMsgLists[self.current_id].insert(tkinter.END, self.txtMsg.get('0.0', tkinter.END))
            self.txtMsg.delete('0.0', tkinter.END)
        except socket.error:
            self.txtMsgLists[self.current_id].insert(tkinter.END, "对方不在线", 'greencolor')

    def send_message_event(self, event):
        if event.keysym == 'Up':
            self.send_message()

    def cancel_message(self):
        self.txtMsg.delete('0.0', tkinter.END)

    def receive_message(self):
        while True:
            try:
                r_msg, ip_port = self.c_socket.recvfrom(1024)
                r_msg = r_msg.decode('utf-8')
                print()
                c_id = self.c_address.index(ip_port)
                str_msg = self.c_id[self.current_id] + '：' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n'
                self.txtMsgLists[c_id].insert(tkinter.END, str_msg, 'greencolor')
                self.txtMsgLists[c_id].insert(tkinter.END, r_msg)
            except socket.timeout:
                pass
            except socket.error:
                self.txtMsgLists[self.current_id].insert(tkinter.END, "对方不在线!", 'greencolor')  # 此处不严谨，未必是当前界面联系人不在线

    def run(self):
        self.root.mainloop()
