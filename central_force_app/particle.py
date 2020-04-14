import numpy as np
from scipy.integrate import solve_ivp


class Particle():
    def __init__(self,
                 mass: float = 1.0,
                 mass_attractive_center: float = 1.0,
                 n_steps_ode: int = int(1e3),
                 exponent: float = -2.0,
                 solver_method: str = 'RK45',
                 ) -> None:
        self._mass = mass
        self._mass_attractive_center = mass_attractive_center
        self._exponent = exponent
        self._solver_method = solver_method
        self._n_steps_ode = n_steps_ode

        # For later caching
        self._r0 = None
        self._v0 = None

    @property
    def mass(self) -> float:
        return self._mass

    @mass.setter
    def mass(self, new_mass: float) -> None:
        self._mass = new_mass

    @property
    def mass_attractive_center(self) -> float:
        return self._mass_attractive_center

    @mass_attractive_center.setter
    def mass_attractive_center(self, new_mass: float) -> None:
        self._mass_attractive_center = new_mass

    @property
    def exponent(self) -> float:
        """Exponent in the central force expression.
        Newtonian gravity is exponent = -2.0.
        """
        return self._exponent

    @exponent.setter
    def exponent(self, new_exponent: float) -> None:
        self._exponent = new_exponent

    @property
    def solver_method(self) -> str:
        return self._solver_method

    @solver_method.setter
    def solver_method(self, new_solver_method: str) -> None:
        self._solver_method = new_solver_method

    @property
    def n_steps_ode(self) -> int:
        return self._n_steps_ode

    @n_steps_ode.setter
    def n_steps_ode(self, new_n_steps_ode: int) -> None:
        self._n_steps_ode = new_n_steps_ode

    def central_force(self, r: float) -> float:
        return -self.mass * self.mass_attractive_center * (r ** self.exponent)

    def _motion_ode(self,
                    t: float,
                    y: np.ndarray
                    ) -> np.ndarray:
        """In polar coordinates: y = (r, r', theta)
        """
        return np.array(
            [
                y[1],
                self.h ** 2 / y[0] ** 3 + self.central_force(y[0])/self.mass,
                self.h / y[0] ** 2,
            ]
        )

    def motion(
        self,
        r0: float,
        drdt0: float,
        theta0: float,
        dthetadt0: float,
        T: float
    ) -> np.ndarray:
        """Integration the motion equations with initial condition:
        r(0) = r0,
        r'(0) = drdt0,
        theta(0) = theta0,
        theta'(0) = dthetadt0,
        for t in [0, T].
        """
        self._r0 = r0
        self._drdt0 = drdt0
        self._theta0 = theta0
        self._dthetadt0 = dthetadt0
        self.h = (self._r0 ** 2) * self._dthetadt0

        solver = solve_ivp(
            self._motion_ode,
            (0.0, T),
            [self._r0, self._drdt0, self._theta0],
            method=self.solver_method,
            t_eval=np.linspace(0.0, T, self.n_steps_ode),
        )

        assert solver.success, 'Integration of deterministic ODEs failed.'

        return solver.t, solver.y
