import matplotlib.pyplot as plt
from SIR import SIR
from RungeKuttaSIR import RungeKuttaSIR
from sys import argv

def simulate(s0,i0,r0,beta,k,dt,tf,output_plt_file):
    # uncomment the line below to use the Forward Euler Method instead of the Runge Kutta and comment the RungKuttaSIR line
    # sir = SIR(s0,i0,r0,beta,k,delta_t,t_final)
    sir = RungeKuttaSIR(s0,i0,r0,beta,k,dt,tf)
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
    plt.savefig(output_plt_file)

def generate_output_plt_name(i):
    return "sir" + str(i) + ".png"

def main():
    file = ""
    s0 = i0 = r0 = beta = k = delta_t = t_final = 0.
    if len(argv) == 2:
        file = argv[1]
    elif len(argv) == 8:
        s0 = float(argv[1])
        i0 = float(argv[2])
        r0 = float(argv[3])
        beta = float(argv[4])
        k = float(argv[5])
        delta_t = float(argv[6])
        t_final = float(argv[7])
    else:
        print("Invalid number of arguments")
        exit(1)

    if file != "":
        with open(file,"rt") as input:
            for i,line in enumerate(input):
                values = line.split(',')
                if len(values) != 7:
                    print("Invalid number of arguments in line %d" % (i + 1))
                    exit(2)

                simulate(float(values[0]),float(values[1]),float(values[2]),float(values[3]),float(values[4]),float(values[5]),float(values[6]),generate_output_plt_name(i))
    else:
        simulate(s0,i0,r0,beta,k,delta_t,t_final,generate_output_plt_name(""))

if __name__ == "__main__":
    main()
    