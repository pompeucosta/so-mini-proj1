from Simulation import Simulation
from Event import Event
import random
from ArrivalEvent import Arrival

class InventorySimulation(Simulation):
    def __init__(self,small_s: int,big_s: int,inv_initial_lvl: int = 60,months: int = 120) -> None:
        super().__init__()
        self._small_s = small_s
        self._big_s = big_s
        self._months = months

        #setup inventory
        self._inv = []
        self._inv_amount = 0
        self._add_items_to_inventory(inv_initial_lvl)

        #statistics
        #costs
        self._order_costs = 0.
        self._express_costs = 0.

        #areas
        self._ipos = 0.
        self._ineg = 0.

        #others
        self._num_express_orders = 0
        self._backlog_time = 0.
        self._num_spoiled_items = 0


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
    
    @property
    def number_of_spoiled_items_discarded(self):
        return self._num_spoiled_items

    def _order_arrival(self):
        elem = self._remove_current_event_from_list()
        amount = elem.amount
        if self._inv_amount >= 0:
            self._add_items_to_inventory(amount)
        else:
            if self._inv_amount + amount > 0:
                added = self._inv_amount + amount
                #if backlog is fullfilled then add the remaining items to inventory
                #ex:
                #inv_amount = -5
                #amount = 6
                #added = -5 + 6 = 1
                #so backlog is fullfilled, then add 1 item to inventory
                self._inv_amount = 0
                self._add_items_to_inventory(added)
            else:
                #backlog is not totaly fullfilled
                self._inv_amount += amount

    def _demand(self):
        self._remove_current_event_from_list()
        amount = random.choices([1,2,3,4],[1/6,1/3,1/3,1/6])[0]
        self._remove_spoiled_items()
        if self._inv_amount > 0:
            if self._inv_amount < amount:
                leftovers = amount - self._inv_amount
                self._remove_inventory_amount(self._inv_amount)
                self._inv_amount -= leftovers
            else:
                self._remove_inventory_amount(amount)
        else:
            self._inv_amount -= amount

        super().events.append(Event("demand",super().sim_time + random.expovariate(10)))

    def _evaluate(self):
        self._remove_current_event_from_list()

        if self._inv_amount < 0:
            #express order
            self._num_express_orders += 1
            amount = self._big_s - self._inv_amount
            self._express_costs += 48 + 4 * amount
            super().events.append(Arrival(amount,super().sim_time + random.uniform(0.25,0.5)))
        elif self._inv_amount < self._small_s:
            amount = self._big_s - self._inv_amount
            self._order_costs += 32 + 3 * amount
            super().events.append(Arrival(amount,super().sim_time + random.uniform(0.5,1)))

        super().events.append(Event("eval",super().sim_time + 1))

    def _update_statistics(self):
        if self._inv_amount == 0:
            return
        
        if self._inv_amount > 0:
            self._ipos += self._inv_amount * (super().sim_time - self._time_last_event)
        else:
            self._ineg += (-self._inv_amount) * (super().sim_time - self._time_last_event)
            self._backlog_time += super().sim_time - self._time_last_event

    def _timing(self):
        self._time_last_event = super().sim_time
        super()._timing()

    def _remove_current_event_from_list(self):
        return super().events.pop(super().current_event_pos)
    
    def _add_items_to_inventory(self,amount: int):
        self._inv_amount += amount
        for _ in range(0,amount):
            self._inv.append(super().sim_time + random.uniform(1.5,2.5))

    def _remove_inventory_amount(self,amount: int):
        for _ in range(0,amount):
            self._remove_item()

    def _remove_spoiled_items(self):
        while len(self._inv) > 0 and self._inv[0] <= super().sim_time:
            self._remove_item()
            self._num_spoiled_items += 1

    def _remove_item(self):
        self._inv_amount -= 1
        self._inv.pop(0)

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