import os
from hashlib import blake2b

def hash_with_blake2b(msg):
    h = blake2b(digest_size=20)
    h.update(bytes(msg, encoding='utf-8'))
    r = h.hexdigest()
    return r

def check_process_exists_or_not(cmd=None, is_return=False):
    stream = os.popen(cmd)
    cmd_output = stream.read()

    if is_return is True:
        return cmd_output
    else:
        if cmd_output:
            description = 'To kill all processes after execution command of `' + cmd + '`'
            print(description)
            exit(0)