import random


def create_input():
    random_id = random.randint(1, 3)
    run_time = random.randrange(1, 10)

    command = f"{random_id} 1 1 1 1 1 1"
    queue_tuple = (command, run_time)

    return queue_tuple

