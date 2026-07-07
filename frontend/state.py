_state: dict = {
    "token": None,
    "tipo":  None,
    "nome":  None,
    "login": None,
}


def set_state(token: str, tipo: str, nome: str, login: str = None):
    _state["token"] = token
    _state["tipo"]  = tipo
    _state["nome"]  = nome
    _state["login"] = login


def get_state(key: str, default=None):
    return _state.get(key, default)


def clear_state():
    _state["token"] = None
    _state["tipo"]  = None
    _state["nome"]  = None
    _state["login"] = None