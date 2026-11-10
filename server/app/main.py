from fastapi import FastAPI, HTTPException, status
from server.app.token_model import Token
from server.app.token_manager import TokenManager
import server.app.database as db



apiApp = FastAPI()
manager = TokenManager()
db.setup_database()

@apiApp.post("/create-token")
def create_token():
    token = Token()
    main_id, disp_id, issued_time = db.add_token(token)

    token.set_id(main_id, disp_id)
    
    position = manager.join(token)
    token.join(issued_time, position)

@apiApp.post("/exit-token")
def leave_token():
    left_token = manager.leave()
    if(left_token == -1):
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail="Cannot Leave: Queue is Empty")

    served_at = db.change_status(left_token.id, "Served")
    left_token.leave(served_at)

    receiving_token = manager.get_receiving_service_token()
    called_at = db.change_status(receiving_token.id, "In Service")
    receiving_token.in_service(called_at)
    

@apiApp.post("/cancel-token/{id}")
def cancel_token(id: str):
    manager.cancel(id)


@apiApp.get("/view", response_model=dict[str,str])
def view_queue():
    return manager.view()

@apiApp.get("/info/{id}")
def get_info(id: str):
    return manager.get_info(id)