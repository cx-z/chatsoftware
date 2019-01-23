# -*- coding:utf-8 -*-
import threading
import Client
import Application


if __name__ == '__main__':
    client1 = Client.Client('1', 10001, 40001)
    client1.bind_address()
    threads = []
    thread = threading.Thread(target=client1.register)
    threads.append(thread)
    thread = threading.Thread(target=client1.get_client_info)
    threads.append(thread)
    app = Application.Application(client1.toClient, 'client1')
    thread = threading.Thread(target=client1.add_peer_to_app, args=(app,))
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
