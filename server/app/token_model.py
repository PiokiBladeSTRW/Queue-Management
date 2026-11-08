import uuid
import time

class Token:

    def __init__(self, last_id, last_queue_pos):
        self.token = uuid.uuid4()
        self.token_id = 'T-' + str(last_id)

        self.status = "Waiting"
        self.pos: int = last_queue_pos

        self.issued_at = time.time()
        self.called_at: float = None
        self.served_at: float = None

    def leave(self):
        self.status = "Served"
        self.served_at = time.time()

    def update_pos(self, pos = -1):
        if(pos != -1):
            return

        self.pos -= 1

        if(self.pos == 0):
            self.status = "In Service"
            self.called_at = time.time()