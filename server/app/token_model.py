import uuid
import time

class Token:

    def __init__(self, last_queue_pos):
        self.id: int
        self.display_id: str

        self.status = "Waiting"
        self.pos: int = last_queue_pos

        self.issued_at = time.time()
        self.called_at: float = None
        self.served_at: float = None

    def set_id(self, main_id:int, display_id:int):
        self.id = main_id
        self.display_id = 'T-' + display_id

    def leave(self):
        self.status = "Served"
        self.served_at = time.time()

    def cancel(self):
        self.status = "Cancelled"

    def update_pos(self, pos = -1):
        if(pos != -1):
            return

        self.pos -= 1

        if(self.pos == 0):
            self.status = "In Service"
            self.called_at = time.time()