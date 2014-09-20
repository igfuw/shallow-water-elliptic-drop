from scipy.integrate import odeint
import matplotlib
#matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt
import sys, getopt


def deriv(y,t):
    # return derivatives of the array y (Eq. 7 written as four 1st order dif. eq.)
    return np.array([y[1], 2. / y[0]**2 / y[2], y[3], 2. / y[0] / y[2]**2])

#solving the set of differential eqs. using the odeint library (based on ODEPACK)
#default value for \lambda_y is 1
#return 2d array: first index - time_steps, 
#second index - [\lambda_x, d \lambda_x / dt, \lambda_y, d \lambda_y / dt]  
def eq_solver(lambx0, time, lamby0=1):
    yinit = np.array([lambx0, 0., lamby0, 0.])
    return odeint(deriv,yinit,time)

def plottin_evol(solut, time, str_name, lamb_lim=None, dotlamb_lim=None):
    #plotting solution   
    fig = plt.figure(1, figsize = (6.5,5.5))
    ax = plt.subplot(1,1,1)
    plt.plot(time, solut[:,0], "g", time, solut[:,2], "b")
    plt.xlabel("time", fontsize=16)
    plt.ylabel(r'$\lambda$',fontsize=20)
    ax.set_ylim(0, lamb_lim)
    #changing ticks' size  
    for item in plt.xticks()[1] + plt.yticks()[1]:
                item.set_fontsize(15)
    ax1 = ax.twinx()
    plt.plot(time, solut[:,1], "g--", time, solut[:,3], "b--")
    plt.ylabel(r'$\dot{\lambda}$', fontsize=20)
    ax1.set_ylim(0, dotlamb_lim)
    #changing ticks' size and removing some of them
    for item in plt.xticks()[1] + plt.yticks()[1]:
        item.set_fontsize(15)
    for i, tick in enumerate(ax.yaxis.get_major_ticks()):
        if i % 2 != 0:
            tick.label1On = False
    for i, tick in enumerate(ax1.yaxis.get_major_ticks()):
        if i %2 != 0:
            tick.label2On = False #2On - labels are on the right side               
    plt.tight_layout()
    plt.savefig(str_name)
    plt.show()

def plotting_evol_ratio(solut, time, str_name, lamb_lim = None, dotlamb_lim = None):
    fig = plt.figure(1, figsize = (6.5,5.5))
    ax = plt.subplot(1,1,1)
    plt.plot(time, solut[:,2] / solut[:,0], "g")
    plt.xlabel("time", fontsize=16)
    plt.ylabel(r'$\lambda_y / \lambda_x$', fontsize=20)
    ax.set_ylim(lamb_lim)
    plt.yticks([0.5,1,1.5,2])
   #changing size of ticks (the plot_settings doesn't work for twinx()                
    for item in plt.xticks()[1] + plt.yticks()[1]:
        item.set_fontsize(15)
    ax1 = ax.twinx()
    plt.plot(time, solut[:,3] / solut[:,1], "g--")
    plt.ylabel(r'$\dot{\lambda}_y / \dot{\lambda}_x$', fontsize=20)
    ax1.set_ylim(dotlamb_lim)
    #settings ticks
    plt.yticks([0.5,1,1.5,2])
    for item in plt.xticks()[1] + plt.yticks()[1]:
        item.set_fontsize(15)
    plt.tight_layout()
    plt.savefig(str_name)
    plt.show()

# the default value for lambx0 is 2
def main(lambx0=2, time_f=10, lamb_lim=None, dotlamb_lim=None):
    #solving differential equations up to the value of time_f for \lambda_x=lambx0
    time = np.linspace(0.0,time_f,time_f*2+1)
    solut = eq_solver(lambx0, time)
    # checking the asymptotic behavior - longer time
    time_asym = np.linspace(0.0, 5*time_f, time_f*4+1)
    solut_asym = eq_solver(lambx0, time_asym)
    
    if lambx0 == 2.:
        plot_name1 = "fig1a.pdf"
        plot_name2 = "fig1b.pdf"
    else:
        #changing pdf's names if called for different values of lambda_{x0}
        plot_name1 = "fig1a_lambx0=" + str(int(lambx0)) + ".pdf"
        plot_name2 = "fig1b_lambx0=" + str(int(lambx0)) + ".pdf" 

    plottin_evol(solut, time, plot_name1)
    plotting_evol_ratio(solut_asym, time_asym, plot_name2)

# the code can be called with following options
if __name__ == "__main__":
    opts, args = getopt.getopt(sys.argv[1:], "l:t:",
                               ["lambx0=", "time_f="])
    arg_dic = {}
    for opt, arg in opts:
        if opt in ("-l", "--lambx0"):
            arg_dic["lambx0"] = float(arg)
        elif opt in ("-t", "--time_f"):
            arg_dic["time_f"] = float(arg)

    # calling the main function with command-line arguments (if any defined)
    main(**arg_dic) 




