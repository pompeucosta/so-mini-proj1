from SIR import SIR

class RungeKuttaSIR(SIR):
    def _update(self):
        s = self._s
        i = self._i
        r = self._r
        dt = self._dt

        k1_s = -self._beta * s * i
        k1_i = self._beta * s * i - self._k * i
        k1_r = self._k * i

        k2_s = -self._beta * (s + 0.5 * dt * k1_s) * (i + 0.5 * dt * k1_i)
        k2_i = self._beta * (s + 0.5 * dt * k1_s) * (i + 0.5 * dt * k1_i) - self._k * (i + 0.5 * dt * k1_i)
        k2_r = self._k * (i + 0.5 * dt * k1_i)

        k3_s = -self._beta * (s + 0.5 * dt * k2_s) * (i + 0.5 * dt * k2_i)
        k3_i = self._beta * (s + 0.5 * dt * k2_s) * (i + 0.5 * dt * k2_i) - self._k * (i + 0.5 * dt * k2_i)
        k3_r = self._k * (i + 0.5 * dt * k2_i)

        k4_s = -self._beta * (s + dt * k3_s) * (i + dt * k3_i)
        k4_i = self._beta * (s + dt * k3_s) * (i + dt * k3_i) - self._k * (i + dt * k3_i)
        k4_r = self._k * (i + dt * k3_i)

        s += (dt / 6) * (k1_s + 2 * k2_s + 2 * k3_s + k4_s)
        i += (dt / 6) * (k1_i + 2 * k2_i + 2 * k3_i + k4_i)
        r += (dt / 6) * (k1_r + 2 * k2_r + 2 * k3_r + k4_r)

        self._s = s
        self._i = i
        self._r = r
