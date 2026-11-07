# Central Queue
import uuid
import time
from fastapi import FastAPI

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
        self.status = "Left"
        self.leave_time = time.time()

    def update_pos(self, pos = -1):
        if(pos != -1):
            return

        self.pos -= 1

        if(self.pos == 0):
            self.called_at = time.time()


class TokenManager:

    def __init__(self):
        self.queue: list[Token] = []
        self.past_tokens: list[Token] = []

        self.last_id = 0

    def join(self, token):
        self.queue.append( token )
        self.last_id += 1

    def leave(self):
        if(self.is_empty()):
            return -1

        leaving_token = self.queue.pop( 0 )

        self.past_tokens.append(leaving_token)
        leaving_token.leave()

        for elem in self.queue:
            elem.update_pos()

    def view(self):
        queue_dict =  {i: self.queue[i].token_id for i in range(self.get_length())}
        return queue_dict


    def get_time_data(self):
        for elem in self.past_tokens:
            if(elem.status == "Left"):
                print(elem.token_id, "->", elem.leave_time - elem.creation_time)

    def is_empty(self):
        return self.get_length() == 0

    def get_length(self):
        return len(self.queue)

            

apiApp = FastAPI()
manager = TokenManager()


@apiApp.post("/create-token")
def create_token():
    manager.join( Token(manager.last_id, manager.get_length()-1) )

@apiApp.post("/exit-token")
def leave_token():
    manager.leave()


@apiApp.get("/view")
def view_queue():
    return manager.view()

@apiApp.get("/time-data")
def get_time_data():
    manager.get_time_data()
