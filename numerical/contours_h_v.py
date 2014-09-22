import sys
sys.path.append("../analytical/")
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import h5py

#reading model output from text file and converting to an array (+transpose)
def reading_modeloutput(filename):
    f = h5py.File(filename, "r")
    h = np.array(f["h"]).transpose()
    qx = np.array(f["qx"]).transpose()
    qy = np.array(f["qy"]).transpose()
    return h, qx, qy 

def contour_plot(ax, isub, var, U, V, x_range, y_range, levels_var=None, annot=None):
    X, Y = np.meshgrid(x_range, y_range)
    plt.subplots_adjust(hspace = 0.)
    plt.subplots_adjust(wspace = 0)
    temp = ticker.MaxNLocator(3)
    #if isub < 2:
    #    ax.set_xticklabels(())
    if isub%2 != 0:
        ax.set_yticklabels(())
    #contour plot for vield
    CS = plt.contourf(X, Y, var,  cmap=plt.cm.Blues, alpha=0.7, levels=levels_var)
    # plotting vectors from U and V fields
    if (U**2+V**2).max() > 0:
        plt.quiver(X[::20, ::20], Y[::20, ::20], U[::20, ::20], V[::20, ::20], 
                   scale=15)
    #cbar = plt.colorbar(CS, fraction=0.04, format="%.1e")
    CS_l = plt.contour(CS, levels=CS.levels,
                       colors = 'k', linewidths=0.2)

    ax.set_ylim(-8.5, 8.5)
    ax.set_xlim(-8.5, 8.5)
    ax.annotate(annot, xy=(0.01, 0.97), xycoords='axes fraction',
                fontsize=12, horizontalalignment='left', 
                verticalalignment='top')

    

# time_hl - list of time levels for reading output and plotting height 
# time_vl - list of time levels for plotting velocity - has to be a subset og time_hl
# dx, dt -  model gridsize and time step
# xy_lim - model domain
# esp - epsilon used to calculate velocity (should be the same as in a simulation)
def main(dir, time_hl=[0, 1, 3, 7], time_vl=[3,7], dt=0.01, dx=0.05, xy_lim=10, 
         casename="fct+iga", eps=1.e-7):

    x_range = y_range = np.arange(-xy_lim, xy_lim, dx)
    h_m_dir = {}
    vx_m_dir = {}
    vy_m_dir = {}

    #reading the model output and savings variables in dictionaries
    for time in time_hl:
        #TODO - thinking about changin the time in hdf names
        time_str = str(int(time/dt))
        if time == 0:
            time_str = time_str + "00"
        h_m, px_m, py_m = reading_modeloutput(dir+"spreading_drop_2delipsa_" + casename + ".out/timestep0000000" + time_str + '.h5')
        #calculating velocity from momentum, only for the droplet area 
        # using numpy masks 
        h_m_dir[time] = np.ma.masked_less(h_m, eps)
        print "time, h max", time, h_m.max()
        vy_m_dir[time] = py_m / h_m_dir[time]
        vx_m_dir[time] = px_m / h_m_dir[time]

    # plotting the height field
    plt.figure(1, figsize = (6,5.8))
    for it, time in enumerate(time_hl):
        levels_h = np.linspace(0, h_m_dir[time].max(), 8)
        ax = plt.subplot(2,2,it+1,aspect='equal')
        contour_plot(ax, it, h_m_dir[time], vx_m_dir[time], vy_m_dir[time],  
                     x_range, y_range, levels_h, 
                     annot="t = "+str(time))
    plt.savefig("fig4.pdf")
    plt.show()

    # plotting the velocity field
    plt.figure(2, figsize = (6,3))
    for it, time in enumerate(time_vl):
        levels_v_cons = np.linspace(0, 1.12, 8)
        v_m = (vx_m_dir[time]**2 +  vy_m_dir[time]**2)**0.5
        ax = plt.subplot(1,2,it+1,aspect='equal')
        contour_plot(ax, it, v_m, vx_m_dir[time], vy_m_dir[time],
                     x_range, y_range, levels_v_cons,
                     annot="t = "+str(time))
    plt.savefig("fig5.pdf")
    plt.show()

# using the model output from numerical directory
main("build/")
