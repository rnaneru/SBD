import redis


class RedisClient:
    def __init__(
            self,
            host='localhost',
            port=6379,
            decode_responses=True
    ):
        self.client = redis.Redis(
            host=host,
            port=port,
            decode_responses=decode_responses
        )

    def set_string(self, key, value):
        try:
            self.client.set(key, value)
        except redis_crud.RedisError as e:
            print(e)
            return None

    def get_string(self, key):
        try:
            return self.client.get(key)
        except redis_crud.RedisError as e:
            print(e)
            return None

    def lpush(self, key, value):
        try:
            self.client.lpush(key, value)
        except redis_crud.RedisError as e:
            print(e)
            return None

    def rpop(self, key):
        try:
            return self.client.rpop(key)
        except redis_crud.RedisError as e:
            print(e)
            return None

    def hset(self, key, mapping):
        try:
            self.client.hset(key, mapping)
        except redis_crud.RedisError as e:
            print(e)
            return None

    def hgetall(self, key):
        try:
            return self.client.hgetall(key)
        except redis_crud.RedisError as e:
            print(e)
            return None


