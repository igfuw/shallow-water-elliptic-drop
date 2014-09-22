import matplotlib
#matplotlib.use('Agg')
from pylab import *
import ellipse_evolution_odeint as el_od
import sys, getopt


def main(lambx0_l=[2,3], time_f=50, partlamb_lim=2.2):
    
    time = np.linspace(0.0,time_f,time_f*2+1)
    solut = {}     
    #solving differential equations up  for lambda_{x0} from the list - lambx0_l
    for lambx0 in lambx0_l:
        solut[str(lambx0)] = el_od.eq_solver(lambx0, time)
    
    #plotting the relation  obtained from energy conservation
    fig = plt.figure(1, figsize = (8.,5))
    ax = plt.subplot(1,1,1)
    #plotting the LHS of eq. 14 for lambda_{x0} = 2 and 3
    plt.plot(time, solut["2"][:,3]**2 + solut["2"][:,1]**2, "g",
             time, solut["3"][:,3]**2 + solut["3"][:,1]**2, "b")
    #plotting the RHS of eq. 14 for lambda_{x0} = 2 and 3  
    plt.plot(time[::2], 4 * (1./2 - 1./solut["2"][::2,2]/solut["2"][::2,0]), "go",
             time[::2], 4 * (1./3 - 1./solut["3"][::2,2]/solut["3"][::2,0]), "bo")
    plt.xlabel("time", fontsize=16)
    plt.ylabel(r'$\dot{\lambda_x}^2 + \dot{\lambda_y}^2$', fontsize=20)
    for item in plt.xticks()[1] + plt.yticks()[1]:
        item.set_fontsize(15)
    ax.set_ylim(0, partlamb_lim)
    ax.set_xlim(0, time_f)
    plt.tight_layout()
    plt.savefig("fig2.pdf")
    plt.show()

# the code can be called with the following options
if __name__ == "__main__":
    opts, args = getopt.getopt(sys.argv[1:], "t:",
                               ["time_f="])
    arg_dic = {}
    for opt, arg in opts:
        if opt in ("-t", "--time_f"):
            arg_dic["time_f"] = float(arg)
        
    # calling the main function with command-line arguments (if any defined)  
    main(**arg_dic) 
