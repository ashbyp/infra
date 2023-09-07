from typing import Any
import redis
from api.API import API


class StashAPI(API):

    def __init__(self, redis_config: dict[Any, Any]) -> None:
        super().__init__()
        self._con = redis.Redis(host=redis_config['host'], port=redis_config['port'], decode_responses=True)

    def ping(self) -> str:
        super().called()
        self._con.set('foo', 'bar')
        return 'round trip successful' if self._con.get('foo') == 'bar' else 'redis may be down'
