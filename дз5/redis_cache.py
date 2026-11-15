import redis


class RedisCache:
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

class LoginCounter:

    def __init__(
            self,
            host='localhost',
            port=6379,
    ):
        self.r = redis.Redis(
            host=host,
            port=port,
            decode_responses=True,
        )

    def check_login(
            self,
            username,
            max_attempts=5,
    ):
