# -*- coding:utf-8 -*-
import tkinter


class Monitor:
    def __init__(self):
        self.peers = []
        self.app = tkinter.Tk()
        self.app.title('注册信息')
        self.win = tkinter.Frame(width=500, height=500, bg='white')
        self.reg_message = tkinter.Text(self.win)
        self.reg_message.tag_config('Indigo', foreground='#4B0082')  # 创建tag
        self.win.grid()
        self.win.grid_propagate(0)
        self.reg_message.grid()

    def update_peers(self, peer_list):  # 更新窗口中的客户端信息
        self.peers = peer_list
        self.reg_message.delete('0.0', tkinter.END)
        for peer in peer_list:
            if peer.state:
                state = '在线'
            else:
                state = '离线'
            table = "client{}\t{}\t{}\t{}\n".format(peer.id, peer.ip, str(peer.port), state)
            self.reg_message.insert(tkinter.END, table, 'Indigo')

    def run(self):
        self.app.mainloop()
