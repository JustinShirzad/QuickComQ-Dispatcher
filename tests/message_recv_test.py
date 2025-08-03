from qcq_dispatch.network.receiver import Receiver

PORT_NUMBER = 50514

def main():
    recv = Receiver(port=PORT_NUMBER)
    while True:
        message,addr = recv.listen()
        print(f"message {message} recv from {addr}")
        
main()