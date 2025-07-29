from multiprocessing import Process, Queue
import time

class dispatch(Process):
    def __init__(self, id = 0, q=None):
        super().__init__()
        self.id = id
        self.q = self.setup_q(q)
        self.command = None
        self.announce_initialisation()

    def announce_initialisation(self):
        print(f"Dispatcher of ID: {self.id} has been created!")

    def setup_q(self, q):
        new_q
        if q is not None:
            new_q = q
        else:
            new_q = Queue()
        return new_q

    def process_q(self):
        while True:
            if not self.q.empty():
                self.command = self.q.get_nowait()
                self.update_message(self.id, self.command[1], self.command[2])
                self.command = None

    def update_message(self, id, command, run_timer):
        robot_id = command.split(" ")
        robot_id = robot_id[0]

        # Run the command for run_timer length if the ids match.
        if robot_id == id:
            self.run_command(command, run_timer)
    
    # Dummy function to be changed later, currently just prints command
    def run_command(self, command, run_timer):
        start_time = time.time()

        while (time.time - start_time < run_timer) and self.q.empty():
            print(command)

    