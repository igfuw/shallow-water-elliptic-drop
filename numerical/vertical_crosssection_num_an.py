import sys
sys.path.append("../analytical/")
import matplotlib.pyplot as plt
import numpy as np
import h5py
import analytic_equations as an_eq


#reading the model output and saving as numpy arrays
def reading_modeloutput(filename):
    f = h5py.File(filename, "r")
    h = np.array(f["h"])
    qx = np.array(f["qx"])
    qy = np.array(f["qy"])
    return h, qx, qy 

#plotting together analytical solution and model output 
def analytic_model_fig(ax, x_range, y_range, h_m, v_m, h_a0, h_a, v_a, 
                       lab_op, annotate_string):
    ax.plot(x_range, h_a, 'b', linewidth=2)
    ax.plot(x_range, h_a0, 'k',
            x_range, h_m, "r")
    ax.set_ylim(-0.6, .6)                
    ax.set_xlim(-8.5, 8.5)     
    plt.ylabel(r'$h$', fontsize=16)                    
    plt.yticks([-0.5,0,.5])
    if "x" in lab_op:
        plt.xlabel(r'    $x$', fontsize=16)
    if "y" in lab_op:
        plt.xlabel(r'    $y$', fontsize=16, position=(0.5,-0.5))
    ax1 = ax.twinx()
    ax1.plot(x_range, 0*x_range, "k--",
             x_range, v_m, "r--", x_range, v_a, 'b--')

    ax1.set_ylim(-1.2, 1.2)
    plt.yticks([-1.,0,1.])                                      
    ax1.set_xlim(-8.5, 8.5)
    if "u" in lab_op:
        plt.ylabel(r'$u$', fontsize=16)
    if "v" in lab_op:
        plt.ylabel(r'$v$', fontsize=16)
    plt.tight_layout()

    ax.annotate(annotate_string, xy=(0.01, 0.97), xycoords='axes fraction',
                fontsize=12, horizontalalignment='left',
                verticalalignment='top')



# time_l - list of time levels for plotting
# dt -  model time step
# xy_lim - model domain
# nxy - number of grid points
# lamb_x0, lamb_y0 - initial values of ellipse axes
def main(dir, casename="fct+iga", lamb_x0=2., lamb_y0=1., time_l=[1,3,7], 
         dt=0.01, nxy=400, xy_lim=10, eps=1.e-7):
    plt.figure(1, figsize = (9,8))
    #plotting comparison between analytic solution and model results 
    for it, time in enumerate(time_l):
        print "plotting for " + casename + ", t = " + str(time)
        #model variables TODO: time
        h_m, px_m, py_m = reading_modeloutput(dir+"spreading_drop_2delipsa_" + casename + ".out/timestep0000000" + str(int(time/dt)) + '.h5')
        # calculate velocity (momentum/height) only in the droplet region.
        vy_m = np.where(h_m>eps, py_m / h_m, 0)
        vx_m = np.where(h_m>eps, px_m / h_m, 0)
        
        # calculating the analatycial solution for t=time
        x_range = y_range = np.linspace(-xy_lim, xy_lim, nxy)
        lamb_ar = an_eq.d2_el_lamb_lamb_t_evol(time, lamb_x0, lamb_y0)
        h_an = an_eq.d2_el_height_plane(lamb_ar[0], lamb_ar[2], x_range, y_range)
        v_an = an_eq.d2_el_velocity_tot_plane(lamb_ar[0], lamb_ar[1], lamb_ar[2],
                                              lamb_ar[3], x_range, y_range)
      
        # calculating depth for t=0
        h_an0 = an_eq.d2_el_height_plane(2, 1, x_range, x_range)        
        # two vertical cross-scections 
        hx_an, hy_an = h_an[nxy/2,:], h_an[:,nxy/2]
        hx_an0, hy_an0 = h_an0[nxy/2,:], h_an0[:,nxy/2]
        vx_an = np.where(hx_an>eps, x_range/lamb_ar[0] * lamb_ar[1],0)
        vy_an = np.where(hy_an>eps, y_range/lamb_ar[2] * lamb_ar[3], 0)

        #plotting xz vertical cross-sections
        ax = plt.subplot(len(time_l),2,2*it+1)
        lab_op = ["u"]
        if it == len(time_l)-1:
            lab_op = lab_op + ["x"]
        analytic_model_fig(ax,
                           np.linspace(-xy_lim, xy_lim, nxy),np.zeros(nxy),
                           h_m[:,nxy/2], vx_m[:, nxy/2], hx_an0, hx_an, vx_an, 
                           lab_op, " t= "+str(time))

        #plotting yz vertical cross-sections
        ax = plt.subplot(len(time_l),2,2*it+2)  
        lab_op = ["v"]
        if it == len(time_l)-1:
            lab_op = lab_op + ["y"]
        analytic_model_fig(ax,
                           np.linspace(-xy_lim, xy_lim, nxy), np.zeros(nxy),
                           h_m[nxy/2,:], vy_m[nxy/2,:], hy_an0, hy_an, vy_an, 
                           lab_op, " t= "+str(time))   

    plt.savefig("fig6.pdf")
    plt.show()

main("build/")

    
    
    
