import uuid
import time

class Token:

    def __init__(self):
        self.id: int
        self.display_id: str
        self.pos: int

        self.status = "Waiting"

        self.issued_at: float

    def set_id(self, main_id:int, display_id:int):
        self.id = main_id
        self.display_id = 'T-' + display_id

    def join(self, issued_at: float, position: int):
        self.pos = position
        self.issued_at = issued_at

        if(self.pos == 0):
            self.status = "In Service"

    def update_pos(self, pos = -1):
        if(pos != -1):
            return

        self.pos -= 1

        if(pos == 0):
            self.status = "In Service"