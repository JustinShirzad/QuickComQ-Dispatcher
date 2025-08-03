from qcq_dispatch.network.receiver import Receiver

PORT_NUMBER = 50514

def main():
    recv = Receiver(port=PORT_NUMBER)
    print(f"RECEIVER CREATED @ {recv.addr}")
    while True:
        message,addr = recv.listen()
        print(f"message {message} recv from {addr}")
        
main()