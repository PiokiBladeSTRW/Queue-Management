# Central Queue
import uuid
import time

class Token:

    def __init__(self, last_id, last_queue_pos):
        self.token = uuid.uuid4()
        self.token_id = 'T-' + str(last_id)

        self.status = "Waiting"
        self.pos: int = last_queue_pos

        self.creation_time = time.time()
        self.leave_time: float = None

    def leave(self):
        self.status = "Left"
        self.leave_time = time.time()

    def update_pos(self, pos = -1):
        if(pos != -1):
            return

        self.pos -= 1


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
        for elem in self.queue:
            print(elem.token_id, end=' ')

        print()

    def is_empty(self):
        return self.get_length() == 0

    def get_length(self):
        return len(self.queue)

    def get_time_data(self):
        for elem in self.past_tokens:
            if(elem.status == "Left"):
                print(elem.token_id, "->", elem.leave_time - elem.creation_time)
            




def main():
    # Setup TokenManager
    manager = TokenManager()

    # Main Testing Loop
    while True:

        # 1. Add Token to Queue, 2. Leave Token, 3. View, 4. Time Study
        c = int(input())

        match c:
            case 1:
                manager.join( Token(manager.last_id, manager.get_length()-1 ))

            case 2:
                manager.leave()

            case 3:
                manager.view()

            case 4:
                manager.get_time_data()

            case _:
                break


# Entry Clause
if (__name__ == "__main__") :
    main()


