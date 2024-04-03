from Event import Event

class Arrival(Event):
    def __init__(self,amount: int, time: float = 0) -> None:
        super().__init__("arrival", time)
        self._amount = amount

    @property
    def amount(self):
        return self._amount