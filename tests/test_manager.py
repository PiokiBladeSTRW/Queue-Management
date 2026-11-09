from server.app.token_manager import TokenManager
from server.app.token_model import Token
from concurrent.futures import ThreadPoolExecutor


def test_join():
    manager = TokenManager()
    token1 = Token(manager.last_id, manager.get_length())

    manager.join(token1)

    assert manager.last_id == 1
    assert manager.queue == [token1]

    token2 = Token(manager.last_id, manager.get_length())

    manager.join(token2)

    assert manager.last_id == 2
    assert manager.queue == [token1, token2]

def test_leave():
    manager = TokenManager()

    for i in range(5):
        token = Token(manager.last_id, manager.get_length())
        manager.join(token)

    manager.leave()
    assert manager.get_length() == 4

    manager.leave()
    assert manager.get_length() == 3

def test_cancel():
    manager = TokenManager()

    token1 = Token(manager.last_id, manager.get_length())
    manager.join(token1)

    token2 = Token(manager.last_id, manager.get_length())
    manager.join(token2)

    token3 = Token(manager.last_id, manager.get_length())
    manager.join(token3)

    
    manager.cancel(token2.id)
    assert manager.queue == [token1, token3]
    assert token3.pos == 1


def test_leave_more_than_tokens():
    manager = TokenManager()

    for i in range(2):
        token = Token(manager.last_id, manager.get_length())
        manager.join(token)

    manager.leave()
    manager.leave()

    assert manager.get_length() == 0
    assert manager.leave() == - 1

def test_cancel_non_existent_token():
    manager = TokenManager()

    for i in range(2):
        token = Token(manager.last_id, manager.get_length())
        manager.join(token)

    manager.cancel("T-0")

    assert manager.get_length() == 1
    assert manager.cancel("T-0") == -1

def test_multi_token_join_together():
    manager = TokenManager()

    def join(_):
        token = Token(manager.last_id, manager.get_length())
        manager.join(token)

        return token

    with ThreadPoolExecutor(max_workers = 50) as pool:
        tokens = list(pool.map(join, range(100)))

    ids = [t.id for t in tokens]
    assert len(set(ids)) == 100
    
