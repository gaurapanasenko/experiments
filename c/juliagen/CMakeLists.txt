cmake_minimum_required(VERSION 3.5)

project(juliagen LANGUAGES C)

add_executable(juliagen main.c)
set_property(TARGET juliagen PROPERTY C_STANDARD 99)
target_link_libraries(juliagen m)
