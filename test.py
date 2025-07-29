from multiprocessing import Process, Queue
from qcq_dispatch import dispatch
import random

def create_queue_entry():
    random_id = random.randint(1, 10)
    random_length = random.randrange(1, 4)

    command = f"{random_id} This_is_a_command"
    queue_tuple = (command, random_length)

    return queue_tuple

def dummy_process(id, queue):
    dispatcher = dispatch(id=id, q=queue)
    dispatcher.process_q

if __name__ == "__main__":
    test_queue = Queue()
    
    # Add some test commands to the queue
    for _ in range(20):
        entry = create_queue_entry()
        test_queue.put(entry)

    a = Process(target=dummy_process, args=(1, test_queue))
    b = Process(target=dummy_process, args=(2, test_queue))
    
    a.start()
    b.start()
    
    a.terminate()
    b.terminate()
    
    a.join()
    b.join()
    
    print("All processes completed.")