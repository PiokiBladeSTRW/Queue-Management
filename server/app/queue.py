# Central Queue

class Queue:

    def __init__(self):
        self.queue = []

    def join(self):
        pass

    def leave(self):
        pass


class Token:

    def __init__(self, last_id):
        self.token = ''
        self.token_id = 'T-' + last_id
        self.pos = 0

    def set_start_pos(self):
        pass

    def update_pos(self):
        pass