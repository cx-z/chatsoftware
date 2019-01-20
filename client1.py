import threading
import Client


if __name__ == '__main__':
    client1 = Client.Client('1', 10001, 40001)
    client1.bind_address()
    threads = []
    thread = threading.Thread(target=client1.register)
    threads.append(thread)
    thread = threading.Thread(target=client1.get_client_info)
    threads.append(thread)
    for t in threads:
        t.start()
    for t in threads:
        t.join()
