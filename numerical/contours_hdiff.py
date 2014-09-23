import sys
sys.path.append("../analytical/")
import matplotlib.pyplot as plt
import numpy as np
import h5py
import analytic_equations as an_eq


#reading model output and saving as numpy arrays
def reading_modeloutput(filename):
    f = h5py.File(filename, "r")
    h = np.array(f["h"]).transpose()
    qx = np.array(f["qx"]).transpose()
    qy = np.array(f["qy"]).transpose()
    return h, qx, qy 

def contour_plot(ax, var, x_range, y_range, levels_var=None):
    X, Y = np.meshgrid(x_range, y_range)
    CS = plt.contourf(X, Y, var,  cmap=plt.cm.Blues, alpha=0.7, levels=levels_var)
    #cbar = plt.colorbar(CS, fraction=0.04, format="%.1e")
    CS_l = plt.contour(CS, levels=CS.levels,
                       colors = 'k', linewidths=0.2)
    ax.set_ylim(-8.5, 8.5)
    ax.set_xlim(-8.5, 8.5)
    

def main(dir, lamb_x0=2., lamb_y0=1., time=7, dt=0.01, dx=0.05, xy_lim=10, 
         casename="fct+iga", eps=1.e-7):
    x_range = y_range = np.arange(-xy_lim, xy_lim, dx)
    time_str = str(int(time/dt))
    h_m, px_m, py_m = reading_modeloutput(dir+"spreading_drop_2delipsa_" + casename + ".out/timestep0000000" + time_str + '.h5')
    #calculating the analytical solution
    lamb_ar = an_eq.d2_el_lamb_lamb_t_evol(time, lamb_x0, lamb_y0)
    h_an = an_eq.d2_el_height_plane(lamb_ar[0], lamb_ar[2], x_range, y_range)
    #the error is normalized by initial height of the drop
    h0_max = 1./ (lamb_x0 * lamb_y0)
    h_diff = abs(h_m - h_an)/h0_max
    print "max of abs(h_m-h_an), h_an.max, h_m.max", abs(h_diff).max(), h_an.max(), h_m.max()
    levels_diff = np.linspace(1.e-7, 2.e-3, 4)
    plt.figure(1, figsize = (3.,3.))
    ax = plt.subplot(1,1,1,aspect='equal')
    contour_plot(ax, h_diff, x_range, y_range, levels_var = levels_diff)
    plt.savefig("fig7.pdf")
    plt.show()

main("build/")
