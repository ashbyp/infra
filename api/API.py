import datetime


class API:
    def __init__(self):
        self._created_at = datetime.datetime.now()
        self._num_calls = 0

    def called(self) -> None:
        self._num_calls += 1

    def num_calls(self) -> int:
        return self._num_calls

    def name(self) -> str:
        return self.__class__.__name__

    def __str__(self):
        return f'{self.name()} has been called {self.num_calls()} times'
