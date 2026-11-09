import time

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

        for token in self.queue:
            token.update_pos()

    def cancel(self, id:str):

        cancel_pos = -1

        for elem in range(self.get_length()):
            if(self.queue[elem].id == id):
                self.queue[elem].cancel()
                self.queue.pop(elem)

                cancel_pos = elem
                break

        if(cancel_pos == -1):
            return -1

        for elem in range(cancel_pos, self.get_length()):
            self.queue[elem].update_pos()            
                

    def view(self):
        queue_dict =  {str(i): self.queue[i].id for i in range(self.get_length())}
        return queue_dict

    def get_length(self):
        return len(self.queue)
    
    def get_info(self, id: str):

        for token in self.queue:
            if(token.id == id):
                return {
                    "ID": token.id,
                    "Position": token.pos,
                    "Status": token.status,
                    "Waiting For": time.time() - token.issued_at
                }

        return -1
    
    def is_empty(self):
        return self.get_length() == 0
