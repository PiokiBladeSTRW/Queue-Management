from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from server.app.token_model import Token
from server.app.token_manager import TokenManager
import server.app.database as db



apiApp = FastAPI()
manager = TokenManager()
db.setup_database()

apiApp.add_middleware(
    CORSMiddleware,
    allow_origins= ["http://127.0.0.1:5500", "http://127.0.0.1:5500"],
    allow_credentials= True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"]
)

class CreateTokenRequest(BaseModel):
    user_name: str = "Guest"


@apiApp.post("/create-token")
def create_token(request: CreateTokenRequest):
    token = Token(request.user_name)
    main_id, disp_id, issued_time = db.add_token(request.user_name)

    token.set_id(main_id, disp_id)
    
    position = manager.join(token)
    token.join(issued_time, position)

    if(position == 0):
        db.change_status(main_id, "In Service")

@apiApp.post("/exit-token")
def leave_token():
    left_token = manager.leave()
    if(left_token == -1):
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail="Cannot Leave: Queue is Empty")

    db.change_status(left_token.id, "Served")

    receiving_token: Token = manager.get_receiving_service_token()
    if(receiving_token != -1):
        db.change_status(receiving_token.id, "In Service")

        return {
            'id': receiving_token.id,
            'disp_id': receiving_token.display_id,
            'user_name': receiving_token.user_name
        }
    

@apiApp.post("/cancel-token/{id}")
def cancel_token(id: int):
    inital_receiving_tok = manager.get_receiving_service_token()

    result = manager.cancel(id)
    if(result == -1):
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail="Invalid User: Doesn't Exist")

    db.change_status(id, "Cancelled")

    final_receiving_tok = manager.get_receiving_service_token()

    if((inital_receiving_tok != final_receiving_tok) and (final_receiving_tok != -1)):
        db.change_status(final_receiving_tok.id, "In Service")




@apiApp.get("/view", response_model=list[dict[str,str|int]])
def view_queue():
    return manager.view()

@apiApp.get("/info/{disp_id}")
def get_info(disp_id: str):
    return manager.get_info(disp_id)