import numpy as np
import cvxpy as cp

class NUMSolver:

    def __init__(self, A, c, f):
        self.n, self.m = A.shape
        self.A = A
        self.c = c
        self.f = f

        print(self.n, self.m)
        assert self.c.size == self.n
        assert len(self.f) == self.m

    def solve(self, coeff):
        assert coeff.size == self.m
        zeroes = (coeff == 0)
        _coeff = np.array([coeff[i] if coeff[i] > 0 else 1 for i in range(self.m)])

        print('coefficients:', coeff)
        print(self.m)

        x = cp.Variable(self.m)
        obj = sum([coeff[i] * self.f[i](x[i] / _coeff[i]) for i in range(self.m)])

        constraints = [x >= 0, self.A @ x <= self.c]

        for i in range(self.m):
            if zeroes[i]:
                constraints += [x[i] == 0]
        prob = cp.Problem(cp.Maximize(obj), constraints)

        prob.solve()

        xs = x.value / _coeff

        print(xs)

        return xs


if __name__ == '__main__':
    import numpy as np
    A = np.mat([[1, 1, 1], [1, 0, 0], [0, 1, 0], [0, 0, 1]])
    c = np.array([10000, 15000, 20000, 10000])
    f = [lambda x: cp.log(x) for i in range(3)]

    solver = NUMSolver(A, c, f)
    xs = solver.solve(np.array([1, 1, 1]))
    print(xs)

    solver = NUMSolver(A, c, f)
    xs = solver.solve(np.array([1, 1, 2]))
    print(xs)

    solver = NUMSolver(A, c, f)
    xs = solver.solve(np.array([0, 0, 2]))
    print(xs)