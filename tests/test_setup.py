def test_imports():
    import pandas, numpy, scipy, statsmodels, sklearn, cvxpy, duckdb, yfinance
    assert "CLARABEL" in cvxpy.installed_solvers()


def test_tiny_optimization():
    import cvxpy as cp
    import numpy as np

    w = cp.Variable(3)
    cov = np.array([[0.04, 0.01, 0.0], [0.01, 0.09, 0.02], [0.0, 0.02, 0.16]])
    prob = cp.Problem(cp.Minimize(cp.quad_form(w, cov)), [cp.sum(w) == 1, w >= 0])
    prob.solve()
    assert prob.status == "optimal"
