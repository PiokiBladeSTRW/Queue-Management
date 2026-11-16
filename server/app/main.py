from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from server.app.token_model import Token
from server.app.token_manager import TokenManager
import server.app.database as db


# Setup
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

# Request Format Specifiers
class CreateTokenRequest(BaseModel):
    user_name: str = "Guest"


# API ENDPOINTS
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

    try:
        left_token = manager.leave()
        db.change_status(left_token.id, "Served")

        receiving_token: Token = manager.get_receiving_service_token()    
        db.change_status(receiving_token.id, "In Service")

        return {
            'id': receiving_token.id,
            'disp_id': receiving_token.display_id,
            'user_name': receiving_token.user_name
        }

    except IndexError as e:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail=e)
    
@apiApp.post("/cancel-token/{id}")
def cancel_token(id: int):
    try:
        inital_receiving_tok = manager.get_receiving_service_token()
        result = manager.cancel(id)
        db.change_status(id, "Cancelled")

        final_receiving_tok = manager.get_receiving_service_token()
        db.change_status(final_receiving_tok.id, "In Service")

    except (IndexError, ValueError) as e:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail=e)




@apiApp.get("/view", response_model=list[dict[str,str|int]])
def view_queue():
    return manager.view()

@apiApp.get("/get_length")
def get_length():
    length = manager.get_length()
    return {"length": length}

@apiApp.get("/get_first")
def get_first_token():
    try:
        receiving_tok = manager.get_receiving_service_token()

        return {
            "id": receiving_tok.id,
            "disp_id": receiving_tok.display_id,
            "user_name": receiving_tok.user_name
        }
    
    except IndexError as e:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail=e)

@apiApp.get("/info/{disp_id}")
def get_info(disp_id: str):
    try:
        return manager.get_info(disp_id)
    
    except ValueError as e:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail=e)