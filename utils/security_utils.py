import bcrypt

PASSWORD_ENCODING = "utf-8"


def hash_pasword(password: str) -> str:
    return bcrypt.hashpw(
        str.encode(password, encoding=PASSWORD_ENCODING), bcrypt.gensalt()
    ).decode(PASSWORD_ENCODING)
