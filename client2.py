import threading
import Client


if __name__ == '__main__':
    client2 = Client.Client('2', 10002, 40002)
    client2.bind_address()
    threads = []
    thread = threading.Thread(target=client2.register)
    threads.append(thread)
    thread = threading.Thread(target=client2.get_client_info)
    threads.append(thread)
    for t in threads:
        t.start()
    for t in threads:
        t.join()
