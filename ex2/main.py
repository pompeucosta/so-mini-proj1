import matplotlib.pyplot as plt
from SIR import SIR
from RungeKuttaSIR import RungeKuttaSIR

def main():
    # TODO: ler valores da linha de comandos
    # valores completamente random
    # TODO: ver valores bons
    s0 = 5
    i0 = 5
    r0 = 5
    beta = 5
    k = 5
    delta_t = 1
    t_final = 5

    sir = RungeKuttaSIR(s0,i0,r0,beta,k,delta_t,t_final)
    sir.simulate()

    susceptible = sir.susceptible
    infected = sir.infected
    recovered = sir.recovered
    time = sir.time

    plt.plot(time,susceptible,label="Susceptible")
    plt.plot(time,infected,label="Infected")
    plt.plot(time,recovered,label="Recovered")
    plt.xlabel("Time")
    plt.ylabel("Population")
    plt.title("SIR")
    plt.legend()
    plt.savefig("sir.png")

if __name__ == "__main__":
    main()
    