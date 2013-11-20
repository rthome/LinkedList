import uuid, hashlib

def _get_salt():
    return str(uuid.uuid4()).replace("-", "")

def _hash_password(password, salt):
    return hashlib.sha512(bytes(salt) + bytes(password)).hexdigest()

def _unpack_passwd(passwd_str):
    salt, hash = str.split(passwd_str, sep="$", maxsplit=1)
    return (salt, hash)

def create_hashed_password(password):
    salt = _get_salt()
    hash = _hash_password(password, salt)
    return "{s}${h}".format(s=salt, h=hash)

def check_password(password, passwd_str):
    salt, hash = _unpack_passwd(passwd_str)
    hashed_password = _hash_password(password, salt)
    return hash == hashed_password
