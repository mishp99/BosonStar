import numpy as np
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt

path_to_script = "../example/complex_vector_star_selfinteracting_solver.py"

# executing the script
exec(open(path_to_script).read())

r = sol['rpos']
m = sol['m']
a1 = sol['a1']
a0 = sol['a0']
da0dr = sol['da0dr']
sigma = sol['sigma']
omega = sol['omega']

# Taking out values close to boundary, since numpy gradient doesn't know about boundary conditions
N_buffer = 10

threshold_MSE = 1e-8

dx = r[1]-r[0]
d2a0dr2 = np.gradient(da0dr, dx)
da1dr = np.gradient(a1, dx)
dsigmadr = np.gradient(sigma, dx)
dmdr =  np.gradient(m, dx)

# Calculating the EM Constraint equation
constraint = np.sqrt(1 - (2*m)/r)*(4*a0**3*cA4*mu**2*r**3 - a0*mu**2*(2*m - r)*r*(-r + a1**2*(8*cA4*m - 4*cA4*r))*sigma**2 + (-2*m + r)**2*sigma*(-(da0dr*dsigmadr*r) + (2*da0dr + d2a0dr2*r - da1dr*omega*r)*sigma + a1*(dsigmadr*omega*r - 2*omega*sigma)))/(2.*r*(-2*m + r)**2*sigma**3)

constraint_MSE = np.square(constraint[N_buffer:-N_buffer]).mean()

# Calculating Hamiltonian constraint equation
ham_constraint = -(-6*a0**4*cA4*GNewton*mu**2*r**4 + a0**2*GNewton*mu**2*(2*m - r)*r**2*(-r + a1**2*(8*cA4*m - 4*cA4*r))*sigma**2 + (-2*m + r)**2*sigma**2*(da0dr**2*GNewton*r**2 - 2*a1*da0dr*GNewton*omega*r**2 - 8*dmdr*sigma**2 + 2*a1**4*cA4*GNewton*mu**2*(-2*m + r)**2*sigma**2 + a1**2*GNewton*r*(-2*m*mu**2*sigma**2 + r*(omega**2 + mu**2*sigma**2))))/(4.*r**2*(-2*m + r)**2*sigma**4)

ham_constraint_MSE = np.square(ham_constraint[N_buffer:-N_buffer]).mean()

assert(constraint_MSE < threshold_MSE)
assert(ham_constraint_MSE < threshold_MSE)
