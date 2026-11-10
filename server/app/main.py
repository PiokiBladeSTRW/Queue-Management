from fastapi import FastAPI
from server.app.token_model import Token
from server.app.token_manager import TokenManager
import server.app.database as db



apiApp = FastAPI()
manager = TokenManager()
db.setup_database()

@apiApp.post("/create-token")
def create_token():
    token = Token(manager.get_length())
    ids = db.add_token(token)

    token.set_id(ids[0], ids[1])
    manager.join(token)

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