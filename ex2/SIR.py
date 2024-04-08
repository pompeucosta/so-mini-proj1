class SIR:
    def __init__(self,s0: int,i0: int,r0: int,beta: float,k: float,dt: float,tf: float) -> None:
        self._susceptible = [s0]
        self._infected = [i0]
        self._recovered = [r0]
        self._time = [0]
        self._beta = beta
        self._k = k
        self._dt = dt
        self._tfinal = tf

        self._sim_time = 0.
        self._s = s0
        self._i = i0
        self._r = r0

    @property
    def susceptible(self):
        return self._susceptible
    
    @property
    def infected(self):
        return self._infected
    
    @property
    def recovered(self):
        return self._recovered
    
    @property
    def time(self):
        return self._time
    
    def _update(self):
        s = self._s - self._beta * self._s * self._i * self._dt
        i = self._i + self._beta * self._s * self._i * self._dt - self._k * self._i * self._dt
        r = self._r + self._k * self._i * self._dt

        self._s = s
        self._i = i
        self._r = r

    def _observe(self):
        self._susceptible.append(self._s)
        self._infected.append(self._i)
        self._recovered.append(self._r)

    def simulate(self):
        while self._sim_time < self._tfinal:
            self._sim_time += self._dt
            self._time.append(self._sim_time)
            self._update()
            self._observe()