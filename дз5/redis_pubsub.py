import redis

import threading, time, json

from datetime import datetime


class RedisPubSub:
    def __init__(
            self,
            host='localhost',
            port=6379,
    ):
        self.publisher = redis.Redis(
            host=host,
            port=port,
            decode_responses=True
        )

        self.subscriber = redis.Redis(
            host=host,
            port=port,
            decode_responses=True
        )

        self.running = False

    def publish_message(self, channel, message):
        try:
            message_json = json.dumps({
                **message,
                'timestamp': datetime.now().isoformat(),
            })
            result = self.publisher.publish(channel, message_json)
            print(
                f'Message published: {message_json}, channel: {channel}, subscribes: {result}'
            )
            return result
        except Exception as e:
            print(e)

    def subscribe_to_channel(self, channel, callback):
        try:
            pubsub = self.subscriber.pubsub()
            pubsub.subscribe(**{channel: callback})
            return pubsub
        except Exception as e:
            print(e)
            return None
        
