project(PackageTest C)
cmake_minimum_required(VERSION 2.8.12)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup(TARGETS)

add_executable(example example.c)
target_link_libraries(example CONAN_PKG::libunwind)

# CTest is a testing tool that can be used to test your project.
if (NOT CMAKE_CROSSCOMPILING)
    enable_testing()
    add_test(
        NAME              example
        WORKING_DIRECTORY ${CMAKE_BINARY_DIR}/bin
        COMMAND           example
    )
endif ()
