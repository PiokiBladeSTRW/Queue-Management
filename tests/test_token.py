from server.app.token_model import Token

def test_creation():
    token = Token(1, 1)

    assert token.pos == 1
    assert token.id == "T-1"
    assert token.status == "Waiting"

def test_pos_update():
    token = Token(1,1)

    token.update_pos()

    assert token.pos == 0
    assert token.status == "In Service"
