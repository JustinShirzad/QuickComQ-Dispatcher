## to test with YAML Sender (that use relative pathing) run it at 1 level up i.e. python3 ./tests/m_processing_test.py
from multiprocessing import Queue,Process
from qcq_dispatch.dispatch import run_dispatcher
from qcq_dispatch.generate_packet import generate_w_interval



if __name__ == "__main__":
    q = Queue()
    input = Process(target=generate_w_interval, args=(q,))
    output = Process(target=run_dispatcher, args=(q,))
    
    input.start()
    output.start()
    
    input.join()
    output.join()
