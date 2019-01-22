import tkinter
import time
import socket


class Application:
    def __init__(self, client_socket, client_id, client_address):
        self.c_socket = client_socket  # 初始化时输入聊天对方的ID、地址和套接字
        self.c_id = client_id
        self.c_address = client_address
        self.root = tkinter.Tk()
        # 创建frame容器
        self.frmLT = tkinter.Frame(width=500, height=320, bg='white')
        self.frmLC = tkinter.Frame(width=500, height=150, bg='white')
        self.frmLB = tkinter.Frame(width=500, height=30)
        self.frmRT = tkinter.Frame(width=200, height=500)
        # 创建控件
        self.txtMsgList = tkinter.Text(self.frmLT)
        self.txtMsgList.tag_config('greencolor', foreground='#008C00')  # 创建tag
        self.txtMsg = tkinter.Text(self.frmLC)
        self.txtMsg.bind("<KeyPress-Up>", self.send_message_event)
        self.btnSend = tkinter.Button(self.frmLB, text='发送', width=8, command=self.send_message)
        self.btnCancel = tkinter.Button(self.frmLB, text='取消', width=8, command=self.cancel_message)

    def create_app(self):
        self.root.title('与{}聊天'.format(self.c_id))
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
        self.txtMsgList.grid()
        self.txtMsg.grid()

    def send_message(self):
        s_msg = self.txtMsg.get('0.0', tkinter.END).encode('utf-8')
        try:
            self.c_socket.sendto(s_msg, self.c_address)
            str_msg = "我:" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n'
            self.txtMsgList.insert(tkinter.END, str_msg, 'greencolor')
            self.txtMsgList.insert(tkinter.END, self.txtMsg.get('0.0', tkinter.END))
            self.txtMsg.delete('0.0', tkinter.END)
        except socket.error:
            self.txtMsgList.insert(tkinter.END, "对方不在线", 'greencolor')

    def send_message_event(self, event):
        if event.keysym == 'Up':
            self.send_message()

    def receive_message_event(self, event):
        self.receive_message()

    def cancel_message(self):
        self.txtMsg.delete('0.0', tkinter.END)

    def receive_message(self):
        while True:
            try:
                r_msg, ip_port = self.c_socket.recvfrom(1024)
                r_msg = r_msg.decode('utf-8')
                if ip_port == self.c_address:
                    str_msg = self.c_id + '：' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n'
                    self.txtMsgList.insert(tkinter.END, str_msg, 'greencolor')
                    self.txtMsgList.insert(tkinter.END, r_msg)
            except socket.timeout:
                pass
            except socket.error:
                self.txtMsgList.insert(tkinter.END, "对方不在线!", 'greencolor')

    def run(self):
        self.root.mainloop()
