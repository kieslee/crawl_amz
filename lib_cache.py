import redis

from conf import r_host, r_port, r_db

pool = None
r = None

def get_cache():
    global pool, r

    if pool is None:
        pool = redis.ConnectionPool(host=r_host, port=r_port, db=r_db, socket_timeout=10)

    r = redis.Redis(connection_pool=pool)
    return r


def get_keys():
    global r
    if r is None:
        r = get_cache()

    return r.keys()


def get_value(k):
    global r
    if r is None:
        r = get_cache()

    return r.get(k)

def set_value(k, v):
    global r
    if r is None:
        r = get_cache()

    r.set(k, v)

#### LIST Operation ####

def list_len(k):
    global r
    if r is None:
        r = get_cache()

    return r.llen(k)


def r_push(k, v):
    global r
    if r is None:
        r = get_cache()

    r.rpush(k, v)


def l_pop(k):
    global r
    if r is None:
        r = get_cache()

    return r.lpop(k)


def l_index(k, index):
    global r
    if r is None:
        r = get_cache()

    return r.lindex(k, index)


def l_rem(k, value):
    global r
    if r is None:
        r = get_cache()

    r.lrem(k, value)
