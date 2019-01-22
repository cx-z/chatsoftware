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

    apps = []
    while True:
        if len(client1.peers) >= 2:
            for item in client1.peers:
                if item.id != client1.id:
                    app = Application.Application(client1.toClient, item.id, (item.ip, item.port))
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
