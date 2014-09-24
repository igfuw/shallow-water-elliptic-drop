Codes for reproducing Figs. 4-7 and Table 2.
===========================================

To compile the code used to obtain the numerical solution presented in the paper,
you need to first obtain the [libmpdata++](http://libmpdataxx.igf.fuw.edu.pl/) package. 
You can clone the library from a [repository](https://github.com/igfuw/libmpdataxx) at github.
If you only want to install the library to run the code (without compiling
the test programs shipped with the library), do the following steps:

    $ git clone http://github.com/slayoo/libmpdataxx
    $ cd libmpdataxx
    $ mkdir build
    $ cd build
    $ cmake ..
    $ sudo cmake -P cmake_install.cmake

After installing libmpdata++ you can run the reference simulation
presented in the paper. After cloning this repository, try:

    $ cd shallow-water-elliptic-drop/numerical
    $ mkdir build
    $ cd build
    $ cmake .. -DCMAKE_BUILD_TYPE=Release
    $ make
    $ ./spreading_drop_2d_el

After running the simulation, you should have a ``spreading_drop_2delipsa_fct+iga.out``
folder with the model output.

For plotting Figs. 4-7, you need Python with scientific libraries 
(e.q. NumPy, SciPy, Matplotlib, h5py). 

Figures 4 and 5 can be obtained by running (from ``shallow-water-elliptic-drop/numerical/``):

    $ python contours_h_v.py

Figure 6 can be obtained by running:

    $ python vertical_crosssection_num_an.py

Figure 7 can be obtained by running:

    $ python contours_hdiff.py


Results from table 2 can be obtained by running:

    $ python errors.py

Results from table 1 can be also obtained by running ``errors.py`` (using the converg_test function), but simulations with various resolutions have to be performed first.  


 
 
