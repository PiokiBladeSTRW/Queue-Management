# Central Queue

class Token:

    def __init__(self, last_id, last_queue_pos):
        self.token = ''
        self.token_id = 'T-' + str(last_id)
        self.pos = last_queue_pos

    def update_pos(self, pos = -1):
        if(pos != -1):
            return

        self.pos -= 1

class TokenManager:

    def __init__(self):
        self.queue = []
        self.last_id = 0

    def join(self, token):
        self.queue.append( token )
        self.last_id += 1

    def leave(self):
        self.queue.pop( 0 )

        for elem in self.queue:
            elem.update_pos()

    def view(self):
        for elem in self.queue:
            print(elem.token_id, end=' ')

    def get_length(self):
        return len(self.queue)



def main():
    # Setup TokenManager
    manager = TokenManager()

    # Main Testing Loop
    while True:
        
        # 1. Add Token to Queue, 2. Leave Token
        c = int(input())

        match c:
            case 1:
                manager.join( Token(manager.last_id, manager.get_length()-1 ))

            case 2:
                manager.leave()

            case 3:
                manager.view()

            case 4:
                break


# Entry Clause
if (__name__ == "__main__") :
    main()


