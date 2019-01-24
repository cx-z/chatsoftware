# -*- coding:utf-8 -*-
import threading
import Client
import Application


if __name__ == '__main__':
    client3 = Client.Client('3', 10003, 40003)
    client3.bind_address()
    threads = []
    thread = threading.Thread(target=client3.register)
    threads.append(thread)
    thread = threading.Thread(target=client3.get_client_info)
    threads.append(thread)
    app = Application.Application(client3.toClient, 'client3')
    thread = threading.Thread(target=client3.add_peer_to_app, args=(app,))
    threads.append(thread)
    thread = threading.Thread(target=app.receive_message)
    threads.append(thread)
    for t in threads:
        t.setDaemon(True)
        t.start()
    app.create_app()
    app.run()
    for t in threads:
        t.join()
