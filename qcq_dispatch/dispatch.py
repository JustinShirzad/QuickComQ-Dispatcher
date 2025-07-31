from multiprocessing import Process, Queue
import time

class dispatch(Process):
    def __init__(self, id=0, q=None):
        super().__init__()
        self.id = id
        self.q = self.setup_q(q)
        self.current_command = None
        self.command_start_time = None
        self.announce_initialisation()
        self.reset_command()

    # Announce that the dispatcher has been created
    def announce_initialisation(self):
        print(f"Dispatcher for ID: {self.id} has been created!")

    # Setup the queue, if not provided, create a new one for testing
    def setup_q(self, q):
        if q is not None:
            return q
        else:
            return Queue()

    # Main processing loop
    def process_q(self):
        while True:
            self.check_new_commands()
            self.handle_command()
            self.check_command_timeout()

    # Get the next command from the queue and keep it if it's id matches
    def check_new_commands(self):
        if not self.q.empty():
            queue_item = self.q.get_nowait()
            command, runtime = queue_item
            
            if self.check_id(self.id, command):
                self.current_command = (command, runtime)
                self.command_start_time = time.time()
                print(f"[Robot {self.id}] New command: '{command}' for duration: {runtime}s")

    # Check if the command has expired
    def check_command_timeout(self):
        if self.current_command is not None:
            command, runtime = self.current_command
            elapsed_time = time.time() - self.command_start_time
            
            if elapsed_time >= runtime:
                print(f"[Robot {self.id}] Command expired, sending RESET")
                self.reset_command()

    # Set a do nothing command to be acted on until a new command replaces it
    def reset_command(self):
        reset_command = f"{self.id} 0 0 0 0 0 0"
        print(f"[Robot {self.id}] Using reset command: '{reset_command}'")
        
        self.current_command = (reset_command, 9999999999999)
        self.command_start_time = time.time()

    # Check if the command is for this robot
    def check_id(self, id, command):
        robot_id = command.split(" ")[0]
        if robot_id == str(id):
            return True
        return False
    
    # Handles the command
    def handle_command(self):
        print(self.current_command)