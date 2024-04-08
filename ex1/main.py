from InventorySimulation import InventorySimulation

def main():
    policies = [(20,40),(20,60),(20,80),(20,100),(40,60),(40,80),(40,100),(60,80),(60,100)]

    print("%9s | %10s | %10s | %10s | %10s | %12s | %12s | %15s" % ("policy","full_cost","order_cost","hold_cost","short_cost","express_cost","backlog_time","express_orders"))
    for small_s,big_s in policies:
        inv_sim = InventorySimulation(small_s,big_s)
        inv_sim.simulate()
        print_sim_results(inv_sim)

def print_sim_results(inv_sim: InventorySimulation):
    policy = inv_sim.policy
    print("(%3d,%3d) | %10.2f | %10.2f | %10.2f | %10.2f | %12.2f | %12.2f | %15d" % (policy[0],policy[1],inv_sim.full_costs,inv_sim.order_cost,inv_sim.hold_costs,inv_sim.short_costs,inv_sim.express_costs,inv_sim.backlog_time,inv_sim.number_of_express_orders))
    # print("(%d,%d): full_cost: %.2f\norder_cost: %.2f\nhold_cost: %.2f\nshort_cost: %.2f\nexpress_cost: %.2f\nbacklog_time: %.2f\nexpress_orders: %d" % (policy[0],policy[1],))

if __name__ == "__main__":
    main()