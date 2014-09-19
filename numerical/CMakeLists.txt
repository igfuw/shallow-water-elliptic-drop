cmake_minimum_required(VERSION 2.8.8) # for OpenMP test to work in C++-only project (see http://public.kitware.com/Bug/view.php?id=11910)
project(libmpdata++ CXX)

include(CheckCXXSourceCompiles)

# C++11
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")
check_cxx_source_compiles("
  #include <type_traits>
  template <bool a, class b> using ei=std::enable_if<a,b>; 
  struct a {a(int){}};struct b:a {using a::a;};  
  int main(){b i(1);}
" CXX11_SUPPORTED)
if (NOT CXX11_SUPPORTED)
  message(FATAL_ERROR "C++11 compatibility test failed - please update your compiler.")
endif()

# Debug mode
set(CMAKE_CXX_FLAGS_DEBUG "-DBZ_DEBUG -g")

# Release mode
if(CMAKE_CXX_COMPILER_ID STREQUAL "GNU" OR CMAKE_CXX_COMPILER_ID STREQUAL "Clang")
  set(CMAKE_CXX_FLAGS_RELEASE "-Wfatal-errors -DNDEBUG -Ofast -march=native")
endif()

# Boost libraries
find_package(Boost COMPONENTS thread date_time system timer filesystem QUIET)
if (NOT Boost_FOUND)
  message(FATAL_ERROR "
  Boost.{Thread,date_time,system,timer,filesystem} not found.
  Please install it (e.g. sudo apt-get install libboost-all-dev).
")
endif()

# locating libmpdata++
check_cxx_source_compiles("
  #include <libmpdata++/solvers/mpdata.hpp>
  int main(){ }
" LIBMPDATAXX_FOUND)
if (NOT LIBMPDATAXX_FOUND)
  message(FATAL_ERROR "libmpdata++ not found")
endif()

add_executable(spreading_drop_2d_el spreading_drop_2d_el.cpp)
target_link_libraries(${test} ${Boost_LIBRARIES})
target_link_libraries(${test} debug "-lblitz")
