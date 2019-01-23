import threading
import Client
import Application


if __name__ == '__main__':
    client2 = Client.Client('2', 10002, 40002)
    client2.bind_address()
    threads = []
    thread = threading.Thread(target=client2.register)
    threads.append(thread)
    thread = threading.Thread(target=client2.get_client_info)
    threads.append(thread)
    app = Application.Application(client2.toClient, 'client2')
    thread = threading.Thread(target=client2.add_peer_to_app, args=(app,))
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
