from fastapi import Query
import hashlib


class SubsonicAuthContext:
    def __init__(self, user):
        self.user = user


def subsonic_auth(
    u: str = Query(...),
    p: str | None = Query(None),
    t: str | None = Query(None),
    s: str | None = Query(None),
    v: str = Query(...),
    c: str = Query(...),
):
    fake_user_db = {
        "admin": {"id": "1", "username": "admin", "password": "admin"}  # в проде хеш!
    }

    user = fake_user_db.get(u)
    #    if not user:
    #        raise_subsonic_error(40, "Wrong username or password")
    #
    #    if p:
    #        if p != user["password"]:
    #            raise_subsonic_error(40, "Wrong username or password")
    #
    #    elif t and s:
    #        expected = hashlib.md5((user["password"] + s).encode()).hexdigest()
    #        if t != expected:
    #            raise_subsonic_error(40, "Wrong username or password")
    #
    #    else:
    #        raise_subsonic_error(10, "Missing credentials")

    return SubsonicAuthContext(user)
