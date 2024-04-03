from InventorySimulation import InventorySimulation

inv_sim = InventorySimulation(20,80)
inv_sim.simulate()

print("full_cost: %.2f\norder_cost: %.2f\nhold_cost: %.2f\nshort_cost: %.2f" % (inv_sim.full_costs,inv_sim.order_cost,inv_sim.hold_costs,inv_sim.short_costs)) 