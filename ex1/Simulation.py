from abc import ABC
from Event import Event
from typing import List

class Simulation(ABC):
    def __init__(self) -> None:
        super().__init__()
        self._events: List[Event] = []
        self._next_event: Event = Event()
        self._sim_time: float = 0.
        self._event_pos: int = 0

    @property
    def current_event_pos(self):
        return self._event_pos
    
    @property
    def sim_time(self):
        return self._sim_time
    
    @property
    def current_event(self):
        return self._next_event

    @property
    def events(self):
        return self._events

    def _timing(self):
        min_time_next_event = 1e9
        for p,e in enumerate(self._events):
            if e.time < min_time_next_event:
                min_time_next_event = e.time
                self._next_event = e
                self._event_pos = p

        self._sim_time = self._next_event.time

    def simulate(self):
        pass
