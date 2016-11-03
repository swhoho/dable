import redis

class MemCache(object):
    def __init__(self):
        self.r = redis.Redis(host = 'ec2-35-161-71-119.us-west-2.compute.amazonaws.com', port = 6379)

    def hold_user_key(self, id, apikey):
        self.r.hset('auth_user',  id, apikey)

    def auth_user(self, id_1, apikey_1):

        if self.r.hget('auth_user', id_1) == apikey_1:
            return True
        else:
            return False
