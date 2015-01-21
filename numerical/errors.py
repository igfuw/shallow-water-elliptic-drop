import sys
sys.path.append("../analytical/")
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


def errors(dir, dt, dx, time_l, xy_lim, casename, eps, lamb_x0=2., lamb_y0=1.):
    x_range = y_range = np.arange(-xy_lim, xy_lim, dx)
    for it, time in enumerate(time_l):
        print "\n", "TIME t = " + str(time), "dx, dt", dx, dt
        time_str = '%0*d' % (10, int(time/dt))
        # reading the mode output
        # TODO: simplify the files names
        import pdb
        pdb.set_trace()

        h_m, px_m, py_m = reading_modeloutput(dir + casename + ".out/timestep" + time_str + '.h5')
        

        # calculating the analytical solution 
        lamb_ar = an_eq.d2_el_lamb_lamb_t_evol(time, lamb_x0=lamb_x0, lamb_y0=lamb_y0)
        h_an = an_eq.d2_el_height_plane(lamb_ar[0], lamb_ar[2], x_range, y_range)
                        
        # calculating the errors of the drop depth, eq. 25 and 26 from the paper
        h_diff = h_m - h_an
        points_nr = h_m.shape[0]*h_m.shape[1]
        print "number of points in the domain, max(h_an), max(h_num)", points_nr, h_an.max(), h_m.max()
        h0_max = 1. / lamb_x0 / lamb_y0
        delh_inf = abs(h_diff).max() / h0_max 
        delh_2 = 1./time * ((h_diff**2).sum() / points_nr )**0.5 

        print "L_inf = max|h_m-h_an|/h_0", delh_inf 
        print "L_2 = sqrt(sum(h_m-h_an)^2 / N) / time", delh_2, "\n"
        
# comparing errors for reference simulation at different time steps
def evolution_test(dir, dt, dx, time_l=[1,3,7], xy_lim=10, 
                   casename="fct+iga", eps=1.e-7):
    errors(dir, dt, dx, time_l, xy_lim, casename, eps)
    
# comparing errors at time=7 for simulations with various resolutions 
def converg_test(dir, time=[7], xy_lim=10, casename="fct+iga", eps=1.e-7):
    errors(dir + "spreading_drop_2delipsa_dx.1_dt.02_", dt=0.02, dx=0.1, time_l=time, xy_lim=xy_lim, casename=casename, eps=eps)
    errors(dir + "spreading_drop_2delipsa_" , dt=0.01, dx=0.05, time_l=time, xy_lim=xy_lim, casename=casename, eps=eps)
    errors(dir + "spreading_drop_2delipsa_dx.025_dt.005_", dt=0.005, dx=0.025, time_l=time, xy_lim=xy_lim, casename=casename, eps=eps)
    errors(dir + "spreading_drop_2delipsa_dx.0125_dt.0025_", dt=0.0025, dx=0.0125, time_l=time, xy_lim=xy_lim, casename=casename, eps=eps) 


evolution_test("build/" + "spreading_drop_2delipsa_" , dt=0.01, dx=0.05)

#converg_test("../libmpdataxx/build/tests/sandbox/spreading_drop_2d_ellipse/wizard/")
