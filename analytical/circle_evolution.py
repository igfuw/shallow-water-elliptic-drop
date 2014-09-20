from scipy.integrate import odeint
from matplotlib import cm
import numpy as np
#TODO uzgdnic ktory analityczny plik sie uzywa
import analytic_eq as eq
import ellipse_evolution_odeint as el_od
import matplotlib.pyplot as plt
import sys, getopt

def main(lamb0=1, time_f=10, lamb_lim=None, dotlamb_lim=None):
    time = np.linspace(0.0,time_f,time_f*2+1)
    # solving differential equations using odeint for axisymmetric and elliptic drops
    solut_cr = el_od.eq_solver(lamb0, time, lamby0=lamb0)
    solut_el = el_od.eq_solver(2*lamb0, time, lamby0=0.5*lamb0)
    # solving analytical eqs. for axisymmetric drop
    lamb_an_cr = eq.d2_lambda_evol(time)
    dotlamb_an_cr = eq.d2_lambda_t_evol(lamb_an_cr)

    #plotting
    fig = plt.figure(1, figsize = (6.5,5.5))
    ax = plt.subplot(1,1,1)
    #plotting a numerical solution for an elliptic drop 
    plt.plot(time, solut_el[:,0], "g", time, solut_el[:,2], "g")
    # plotting a numerical and an analytical solution for an axisymmetric drop
    plt.plot(time, solut_cr[:,0], "r", time, lamb_an_cr, "r o")
    plt.xlabel("time", fontsize=16) 
    plt.ylabel(r'$\lambda$    ',fontsize=20)
    ax.set_ylim(0, lamb_lim)
    for item in plt.xticks()[1] + plt.yticks()[1]:
        item.set_fontsize(15)
    ax1 = ax.twinx()
    #plotting d lambda / dt in the same way as lambda
    plt.plot(time, solut_el[:,1], "g--", time, solut_el[:,3], "g--")
    plt.plot(time, solut_cr[:,1], "r--", time, dotlamb_an_cr, "r o")
    for item in plt.xticks()[1] + plt.yticks()[1]:
        item.set_fontsize(15)
    for i, tick in enumerate(ax.yaxis.get_major_ticks()):
        if i % 2 != 0:
            tick.label1On = False 
    plt.ylabel(r'$\dot{\lambda}$    ', fontsize=20)
    ax1.set_ylim(0, dotlamb_lim)
    plt.tight_layout()
    plt.savefig("fig3.pdf")
    plt.show()

# the code can be call with following options
if __name__ == "__main__":
    opts, args = getopt.getopt(sys.argv[1:], "l:t:",
                               ["lambx0=", "time_f="])
    arg_dic = {}
    for opt, arg in opts:
        if opt in ("-l", "--lambx0="):
            arg_dic["lambx0"] = float(arg)
        elif opt in ("-t", "--time_f"):
            arg_dic["time_f"] = float(arg)

    main(**arg_dic) 




