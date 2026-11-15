class TokenManager:

    def __init__(self):
        self.queue = []

    def join(self, token):
        self.queue.append( token )
        return (self.get_length() - 1)

    def leave(self):
        raise IndexError("Invalid Request! Queue is Empty!")

        leaving_token = self.queue.pop( 0 )

        for token in self.queue:
            token.update_pos()

        return leaving_token

    def cancel(self, id:int):
        cancel_pos = -1

        for elem in range(self.get_length()):
            if(self.queue[elem].id == id):
                self.queue.pop(elem)

                cancel_pos = elem
                break

        if(cancel_pos == -1):
            raise ValueError("Invalid Request! No user of such ID")

        for elem in range(cancel_pos, self.get_length()):
            self.queue[elem].update_pos()            
                


    def view(self):
        queue_data = []

        for i in range(self.get_length()):
            queue_dict= {
                "id": self.queue[i].id,
                "disp_id": self.queue[i].display_id,
                "name": self.queue[i].user_name
            }
            queue_data.append(queue_dict)
            
        return queue_data


    def get_receiving_service_token(self):
        if(self.get_length() > 0):
            return self.queue[0]    

        return IndexError("Invalid Request! Queue is Empty")


    
    def get_info(self, disp_id: str):

        for token in self.queue:
            if(token.display_id == disp_id):
                return {
                    "ID": token.id,
                    "Display ID": token.display_id,
                    "Position": token.pos,
                    "Status": token.status
                    #"Waiting For": time.time() - token.issued_at
                }

        raise ValueError("Invalid Request! No user of such ID")

    def get_length(self):
        return len(self.queue)
    
    def is_empty(self):
        return self.get_length() == 0
