cmake_minimum_required(VERSION 3.17)
set(CMAKE_CXX_STANDARD 14)
project(OS)

set(kerneldir "")
if("$(kerneldir)" STREQUAL "")
    execute_process(COMMAND uname -r OUTPUT_VARIABLE uname_r OUTPUT_STRIP_TRAILING_WHITESPACE)
    set(kerneldir "/lib/modules/$(uname_r)/build")
endif()

find_file(kernel_makefile NAMES Makefile
        PATHS ${kerneldir} NO_DEFAULT_PATH)

if(NOT kernel_makefile)
    message(FATAL_ERROR "There is no Makefile in kerneldir!")
endif()

# gather the sourse files
add_library(mymodule-lib STATIC camera.cpp)
get_target_property(module_sources mymodule-lib SOURCES)
list(APPEND module_sources module.c)

# generate a Kbuildfile
string(REPLACE ";" " " module_sources_string "${module_sources}")
configure_file(Kbuild.in Kbuild @ONLY)

# Make the source files accessible to the kernel Makefile
foreach(src ${module_sources})
    configure_file(${src} ${src} COPYONLY)
endforeach()

# Add a custom target to build the module
set(module_cmd ${CMAKE_MAKE_PROGRAM} -C ${kerneldir} M=${CMAKE_CURRENT_BINARY_DIR})
add_custom_command(OUTPUT mymodule.ko
        COMMAND ${module_cmd} modules
        WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
        DEPENDS ${module_sources} ${CMAKE_CURRENT_BINARY_DIR}/Kbuild
        VERBATIM)
add_custom_target(module DEPENDS mymodule.ko)
add_custom_target(module-clean COMMAND ${module_cmd} clean)

# OPENCV
find_package( OpenCV REQUIRED )
include_directories( ${OpenCV_INCLUDE_DIRS} )
target_link_libraries( DisplayImage ${OpenCV_LIBS})