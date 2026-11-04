# Central Queue

class Queue:

    def __init__(self):
        self.queue = []

    def join(self, token):
        self.queue.append( token.token_id )

    def leave(self):
        self.queue.pop( 0 )

    def view(self):
        for elem in self.queue:
            print(elem)

    def get_length(self):
        return len(self.queue)


class Token:

    def __init__(self, last_id):
        self.token = ''
        self.token_id = 'T-' + str(last_id)
        self.pos = 0

    def set_start_pos(self, queue_pos):
        self.pos = queue_pos

    def update_pos(self, pos = -1):
        if(pos != -1):
            return

        self.pos -= 1

tokens = []
last_id = 0

queue = Queue()

while True:
    # 1. Add Token to Queue, 2. Leave Token
    c = int(input())

    match c:
        case 1:
            temp_token = Token(last_id)
            last_id += 1

            tokens.append(temp_token)
            queue.join(temp_token)
            
            temp_token.set_start_pos(queue.get_length() - 1)

        case 2:
            queue.leave()
            for temp_token in tokens:
                temp_token.update_pos()

        case 3:
            queue.view()

        case 4:
            break

        case _:
            print("0")
