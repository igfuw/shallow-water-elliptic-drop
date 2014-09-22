import numpy as np
import math
from scipy.optimize import fsolve
from scipy.integrate import odeint


# *** equations for 3D axisymmetric droplet (spreading on 2D plane under gravity)

def d2_rad2(x,y):
    return x**2 + y**2
 
# eq. 21 (Jarecka, Jaruga, Smolarkiewicz)
def d2_lambda_evol(lamb0, time):
    return (2*time**2 + lamb0**2)**0.5

# eq. 15 (Jarecka, Jaruga, Smolarkiewicz) 
def d2_height(lamb, x, y):
    return np.where(d2_rad2(x,y) <= lamb**2, lamb**-2 * (1. - d2_rad2(x,y)/lamb**2), 0)

# eq. 20 (Jarecka, Jaruga, Smolarkiewicz) 
def d2_dot_lambda(lamb, lamb0):
    return 2**0.5 * (lamb0**-2 - lamb**-2)**0.5

# eq. 16 (Jarecka, Jaruga, Smolarkiewicz) for u (since depends on x)  
def d2_velocity(lamb, lamb0, x, y):
    dot_lamb_t = d2_dot_lambda(lamb, lamb0)
    return np.where(d2_rad2(x,y) <= lamb**2, x * dot_lamb / lamb, 0)

# \sqrt(u^2 + v^2) 
def d2_velocity_tot(lamb, lamb0, x, y):
    dot_lamb = d2_dot_lambda(lamb, lamb0)
    v_tot = ((x * dot_lamb / lamb)**2 +  (y * dot_lamb / lamb)**2)**0.5
    return np.where(d2_rad2(x,y) <= lamb**2, v_tot, 0)



#  *** equations for 3D elliptic droplet (spreading on 2D plane under gravity) 

# eq. 5 (Jarecka, Jaruga, Smolarkiewicz)
def d2_el_height_plane(lamb_x, lamb_y, x, y):
    X, Y = np.meshgrid(x, y)
    return np.where(X**2/lamb_x**2 + Y**2/lamb_y**2 <= 1.,
                    1./lamb_x/lamb_y * (1. - X**2/lamb_x**2 - Y**2/lamb_y**2), 0.)

# eq. 6 (Jarecka, Jaruga, Smolarkiewicz)
def d2_el_velocity_tot_plane(lambx, lambx_t, lamby, lamby_t, x, y):
    X, Y = np.meshgrid(x, y)
    v_tot = ( (X * lambx_t / lambx)**2 + (Y * lamby_t / lamby)**2 )**0.5
    return np.where(X**2/lambx**2 + Y**2/lamby**2 <= 1., v_tot, 0)


# return derivatives of [lambda_x, dlambda_x/dt, lambda_y, dlambda_y/dt  
def deriv(y,t):
    # four first-order ODEs based on  eq. 7  (Jarecka, Jaruga, Smolarkiewicz)
    return np.array([y[1], 2. / y[0]**2 / y[2], y[3], 2. / y[0] / y[2]**2])

# solving coupled nonlinear second-order ODEs - eq. 7  (Jarecka, Jaruga, Smolarkiewicz)
# returning array - [\lambda_x, \dot{\lambda_x}, \lambda_y, \dot{\lambda_y}
def d2_el_lamb_lamb_t_evol(time, lamb_x0, lamb_y0, dt=0.01):
    nt_step = time / dt
    time_lin = np.linspace(0.0,time,nt_step)
    yinit = np.array([lamb_x0, 0., lamb_y0, 0.]) # initial values (dot_lamb = 0.)
    # using odeint from scipy.integrate - an implementation of 
    #the LSODA method from the ODEPACK library
    y = odeint(deriv,yinit,time_lin)
    # returning only solution after t=time 
    return y[-1,:]
