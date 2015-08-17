/**
 * @file
 * @copyright University of Warsaw
 * @section LICENSE
 * GPLv3+ (see the COPYING file or http://www.gnu.org/licenses/)
 */

#include <libmpdata++/solvers/shallow_water.hpp>  // solver choice
#include <libmpdata++/concurr/threads.hpp>        // concurrency handler
#include <libmpdata++/output/hdf5_xdmf.hpp>       // output mechanism
using namespace libmpdataxx; 

#include <boost/math/constants/constants.hpp>
using boost::math::constants::pi;

#include <fstream>

const int 
  nt = 700,       // number of time steps
  outfreq = 100;  // output frequency

using real_t = double;  //floating point format used within the simulation

// initial condition
struct intcond
{
  real_t operator()(const real_t &x, const real_t &y) const
  {
    return 
      x*x/4. + y*y <= 1             // if
      ? 1./2. * (1 - x*x/4. - y*y)  // then
      : 0;                          // else
  }
  BZ_DECLARE_FUNCTOR2(intcond);
};

template <int opts_arg>
void test(const std::string &outdir) 
{
  // compile-time parameters 
  // see sec. 3.2.1 in Jaruga et al 2014 http://arxiv.org/abs/1407.1309v2
  struct ct_params_t : ct_params_default_t
  {
    using real_t = ::real_t;
    enum { n_dims = 2 };
    enum { n_eqns = 3 };
    
    // options
    enum { opts = opts_arg | opts::dfl };  // advection scheme options - see sec. 3 in Jaruga et al 2014
    enum { rhs_scheme = solvers::trapez }; // RHS options - see sec. 4 in Jaruga et al 2014

    // indices
    struct ix { enum {
	qx, qy, h, 
	vip_i=qx, vip_j=qy, vip_den=h
    }; }; 
    
    // hints
    enum { hint_norhs = opts::bit(ix::h) }; // hint for no sources for drop height - see sec. 5.3 in Jaruga et al 2014
  };

  using ix = typename ct_params_t::ix;

  // solver choice
  using solver_t = output::hdf5_xdmf<solvers::shallow_water<ct_params_t>>;

  // run-time parameters
  typename solver_t::rt_params_t p; 

  p.dt = .01;
  p.di = .05;
  p.dj = .05;
  p.grid_size = { int(20 / p.di), int(20 / p.dj) };
  p.g = 1;
  p.outfreq = outfreq;
  p.outdir = outdir;
  p.outvars = {
    {ix::h,  {.name="h" , .unit="TODO"}}, 
    {ix::qx, {.name="qx", .unit="TODO"}}, 
    {ix::qy, {.name="qy", .unit="TODO"}}
  };
  p.vip_eps = 1e-7;  // epsilon for velocity interpolation - see sec. 5.3 in Jaruga et al 2014

  // instantiation
  concurr::threads<
    solver_t, 
    bcond::cyclic, bcond::cyclic,
    bcond::cyclic, bcond::cyclic
  > run(p); 

  // initial condition ...
  {
    blitz::firstIndex i;
    blitz::secondIndex j;
    //... for drop height ...
    run.advectee(ix::h) = intcond()(
      p.di * i - (p.grid_size[0]-1) * p.di / 2, 
      p.dj * j - (p.grid_size[1]-1) * p.dj / 2
    );
  }
  // ... and momenta 
  run.advectee(ix::qx) = 0;
  run.advectee(ix::qy) = 0;

  // run the simulation
  run.advance(nt);
};

int main()
{
  test<opts::fct | opts::iga>("spreading_drop_2delipsa_fct+iga.out");
}

