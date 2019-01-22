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

    apps = []
    while True:
        if client2.peers:
            for item in client2.peers:
                app = Application.Application(client2.toClient, item.id, (item.ip, item.port))
                thread = threading.Thread(target=app.receive_message)
                threads.append(thread)
                apps.append(app)
            break
        else:
            continue

    for t in threads:
        t.setDaemon(True)
        t.start()

    for a in apps:
        a.create_app()
        a.run()

    for t in threads:
        t.join()
