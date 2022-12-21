from os.path import abspath
from pathlib import Path
import sys
sys.path.append(abspath(Path(__file__, "../../")))

from hashlib import blake2b
from base64 import b64encode
from env import config

def maeke_hash_key(data):
    hashed = blake2b(data.encode(), key=config.HASH_KEY, digest_size=6)
    b64 = b64encode(hashed.digest())
    return b64.decode()

def make_hashed_pw(password):
    hashed = blake2b(password.encode(), key=config.PW_HASH_KEY, digest_size=64)
    return hashed.hexdigest()

if __name__ == "__main__":
    hash_key = maeke_hash_key("asdf")
    print(hash_key)
    hashed_pw = make_hashed_pw("qwer")
    print(hashed_pw)