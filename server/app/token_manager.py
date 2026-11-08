class TokenManager:

    def __init__(self):
        self.queue = []
        self.last_id = 0

    def join(self, token):
        self.queue.append( token )
        self.last_id += 1

    def leave(self):
        if(self.is_empty()):
            return -1

        leaving_token = self.queue.pop( 0 )
        leaving_token.leave()

        for elem in self.queue:
            elem.update_pos()

    def view(self):
        queue_dict =  {str(i): self.queue[i].token_id for i in range(self.get_length())}
        return queue_dict

    def is_empty(self):
        return self.get_length() == 0

    def get_length(self):
        return len(self.queue)
