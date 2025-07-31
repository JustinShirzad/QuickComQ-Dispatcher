from multiprocessing import Process, Queue
from qcq_dispatch import dispatch
import random
import time

def create_queue_entry():
    random_id = random.randint(1, 3)
    random_length = random.randrange(1, 10)

    command = f"{random_id} 1 1 1 1 1 1"
    queue_tuple = (command, random_length)

    return queue_tuple

def dummy_process(id, queue):
    dispatcher = dispatch(id=id, q=queue)
    dispatcher.process_q()

if __name__ == "__main__":
    test_queue = Queue()

    a = Process(target=dummy_process, args=(1, test_queue))
    
    a.start()

    # Add some test commands to the queue after a random delay
    for _ in range(30):
        entry = create_queue_entry()
        test_queue.put(entry)
        random_sleep_time = random.uniform(0.1, 2.0)
        time.sleep(random_sleep_time)
    
    a.terminate()
    
    a.join()
    
    print("\nAll processes completed.")