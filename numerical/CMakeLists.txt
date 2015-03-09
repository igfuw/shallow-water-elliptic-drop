cmake_minimum_required(VERSION 2.8.8) # for OpenMP test to work in C++-only project (see http://public.kitware.com/Bug/view.php?id=11910)
project(shallow-water-elliptic-drop CXX)

find_package(libmpdata++)
if (NOT libmpdataxx_FOUND) 
  message(FATAL_ERROR "libmpdata++ not found")
endif()

if(NOT CMAKE_BUILD_TYPE STREQUAL "Debug")
  set(CMAKE_CXX_FLAGS ${libmpdataxx_CXX_FLAGS_RELEASE})
  set(CMAKE_CXX_FLAGS_RELEASE "")
else()
  set(CMAKE_CXX_FLAGS_DEBUG ${libmpdataxx_CXX_FLAGS_DEBUG})
endif()

add_executable(spreading_drop_2d_el spreading_drop_2d_el.cpp)
target_link_libraries(spreading_drop_2d_el ${libmpdataxx_LIBRARIES})
target_link_libraries(spreading_drop_2d_el debug "-lblitz")
