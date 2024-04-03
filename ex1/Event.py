class Event:
    def __init__(self,type: str = "",time: float = 0) -> None:
        self._event_type : str = type
        self._event_time : float = time

    @property
    def type(self):
        return self._event_type

    @property
    def time(self):
        return self._event_time
