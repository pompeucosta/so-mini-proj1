from Event import Event

class Arrival(Event):
    def __init__(self,amount: int, type: str = "", time: float = 0) -> None:
        super().__init__(type, time)
        self._amount = amount

    @property
    def amount(self):
        return self._amount