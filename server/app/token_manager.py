class TokenManager:

    def __init__(self):
        self.queue = []
        self.past_tokens = []

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
        queue_dict =  {str(i): self.queue[i].token_id for i in range(self.get_length())}
        return queue_dict


    def get_time_data(self):
        for elem in self.past_tokens:
            if(elem.status == "Left"):
                print(elem.token_id, "->", elem.leave_time - elem.creation_time)

    def is_empty(self):
        return self.get_length() == 0

    def get_length(self):
        return len(self.queue)
