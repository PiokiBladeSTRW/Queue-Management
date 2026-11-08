from fastapi import FastAPI
from server.app.token_model import Token
from server.app.token_manager import TokenManager



apiApp = FastAPI()
manager = TokenManager()


@apiApp.post("/create-token")
def create_token():
    manager.join( Token(manager.last_id, manager.get_length()-1) )

@apiApp.post("/exit-token")
def leave_token():
    manager.leave()

@apiApp.post("/cancel-token/{id}")
def cancel_token(id: str):
    manager.cancel(id)


@apiApp.get("/view", response_model=dict[str,str])
def view_queue():
    return manager.view()

@apiApp.get("/info/{id}")
def get_info(id: str):
    return manager.get_info(id)