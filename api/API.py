import datetime


class API:
    def __init__(self):
        self._created_at = datetime.datetime.now()
        self._num_calls = 0

    def called(self):
        self._num_calls += 1