from Simulation import Simulation
from Event import Event
import random
from ArrivalEvent import Arrival

class InventorySimulation(Simulation):
    def __init__(self,small_s: int,big_s: int,inv_lvl: int = 60,months: int = 120) -> None:
        super().__init__()
        self._small_s = small_s
        self._big_s = big_s
        self._inv_lvl = inv_lvl
        self._months = months

        #statistics
        #costs
        self._order_costs = 0.
        self._express_costs = 0.

        #areas
        self._ipos = 0.
        self._ineg = 0.

        self._num_express_orders = 0
        self._backlog_time = 0.

        #initialize events
        super().events.append(Event("eval",0))
        super().events.append(Event("demand",random.expovariate(10)))
        super().events.append(Event("end",months))

        self._time_last_event : float = 0.

    @property
    def policy(self):
        return (self._small_s,self._big_s)

    @property
    def order_cost(self):
        return self._order_costs / self._months
    
    @property
    def hold_costs(self):
        return self._ipos / self._months
    
    @property
    def short_costs(self):
        return self._ineg * 5 / self._months
    
    @property
    def full_costs(self):
        return self.order_cost + self.hold_costs + self.short_costs + self.express_costs
    
    @property
    def express_costs(self):
        return self._express_costs / self._months
    
    @property
    def backlog_time(self):
        return self._backlog_time
    
    @property
    def number_of_express_orders(self):
        return self._num_express_orders

    def _order_arrival(self):
        elem = self._remove_current_event_from_list()
        self._inv_lvl += elem.amount

    def _demand(self):
        self._remove_current_event_from_list()
        amount = random.choices([1,2,3,4],[1/6,1/3,1/3,1/6])[0]
        self._inv_lvl -= amount
        super().events.append(Event("demand",super().sim_time + random.expovariate(10)))

    def _evaluate(self):
        self._remove_current_event_from_list()

        if self._inv_lvl < 0:
            #express order
            self._num_express_orders += 1
            amount = self._big_s - self._inv_lvl
            self._express_costs += 48 + 4 * amount
            super().events.append(Arrival(amount,super().sim_time + random.uniform(0.25,0.5)))
            pass
        elif self._inv_lvl < self._small_s:
            amount = self._big_s - self._inv_lvl
            self._order_costs += 32 + 3 * amount
            super().events.append(Arrival(amount,super().sim_time + random.uniform(0.5,1)))

        super().events.append(Event("eval",super().sim_time + 1))

    def _update_statistics(self):
        if self._inv_lvl == 0:
            return
        
        if self._inv_lvl > 0:
            self._ipos += self._inv_lvl * (super().sim_time - self._time_last_event)
        else:
            self._ineg += (-self._inv_lvl) * (super().sim_time - self._time_last_event)
            self._backlog_time += super().sim_time - self._time_last_event

    def _timing(self):
        self._time_last_event = super().sim_time
        super()._timing()

    def _remove_current_event_from_list(self):
        return super().events.pop(super().current_event_pos)
    
    def simulate(self):
        while(super().current_event.type != "end"):
            self._timing()
            self._update_statistics()

            if super().current_event.type == "arrival":
                self._order_arrival()
            elif super().current_event.type == "demand":
                self._demand()
            elif super().current_event.type == "eval":
                self._evaluate()