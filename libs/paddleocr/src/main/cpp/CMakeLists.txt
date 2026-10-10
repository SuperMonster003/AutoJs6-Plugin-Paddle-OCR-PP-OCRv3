# For more information about using CMake with Android Studio, read the
# documentation: https://d.android.com/studio/projects/add-native-code.html

# Sets the minimum version of CMake required to build the native library.

cmake_minimum_required(VERSION 3.22.1)

# Creates and names a library, sets it as either STATIC or SHARED, and provides
# the relative paths to its source code. You can define multiple libraries, and
# CMake builds them for you. Gradle automatically packages shared libraries with
# your APK.

get_filename_component(MODULE_DIR "${CMAKE_CURRENT_LIST_DIR}/../../.." ABSOLUTE)
set(PaddleLite_DIR "${MODULE_DIR}/PaddleLite")
include_directories(${PaddleLite_DIR}/cxx/include)

# Private OpenCV: static libraries of the official OpenCV Android SDK (TBB backend, no OpenMP).
# The version script below keeps every OpenCV symbol local to libNative.so.
if (NOT DEFINED OPENCV_SDK_NATIVE_DIR)
    message(FATAL_ERROR "OPENCV_SDK_NATIVE_DIR must point to sdk/native of the verified OpenCV Android SDK")
endif ()
set(OpenCV_DIR "${OPENCV_SDK_NATIVE_DIR}/jni")
message(STATUS "opencv dir: ${OpenCV_DIR}")
find_package(OpenCV REQUIRED COMPONENTS core imgproc imgcodecs)
if (OpenCV_SHARED)
    message(FATAL_ERROR "libNative.so must link the static OpenCV libraries")
endif ()
message(STATUS "OpenCV libraries: ${OpenCV_LIBS}")
include_directories(${OpenCV_INCLUDE_DIRS})
aux_source_directory(. SOURCES)
set(CMAKE_CXX_FLAGS
        "${CMAKE_CXX_FLAGS} -ffast-math -Ofast -Os"
        )
set(CMAKE_CXX_FLAGS
        "${CMAKE_CXX_FLAGS} -fvisibility=hidden -fvisibility-inlines-hidden -fdata-sections -ffunction-sections"
        )
set(CMAKE_SHARED_LINKER_FLAGS
        "${CMAKE_SHARED_LINKER_FLAGS} -Wl,--gc-sections -Wl,-z,nocopyreloc")

add_library(
        # Sets the name of the library.
        Native
        # Sets the library as a shared library.
        SHARED
        # Provides a relative path to your source file(s).
        ${SOURCES})

find_library(
        # Sets the name of the path variable.
        log-lib
        # Specifies the name of the NDK library that you want CMake to locate.
        log)

add_library(
        # Sets the name of the library.
        paddle_light_api_shared
        # Sets the library as a shared library.
        SHARED
        # Provides a relative path to your source file(s).
        IMPORTED)

set_target_properties(
        # Specifies the target library.
        paddle_light_api_shared
        # Specifies the parameter you want to define.
        PROPERTIES
        IMPORTED_LOCATION
        ${PaddleLite_DIR}/cxx/libs/${ANDROID_ABI}/libpaddle_light_api_shared.so
        # Provides the path to the library you want to import.
)


# Specifies libraries CMake should link to your target library. You can link
# multiple libraries, such as libraries you define in this build script,
# prebuilt third-party libraries, or system libraries.

target_link_libraries(
        # Specifies the target library.
        Native
        paddle_light_api_shared
        ${OpenCV_LIBS}
        GLESv2
        EGL
        jnigraphics
        ${log-lib}
)

add_custom_command(
        TARGET Native
        POST_BUILD
        COMMAND
        ${CMAKE_COMMAND} -E copy
        ${PaddleLite_DIR}/cxx/libs/${ANDROID_ABI}/libc++_shared.so
        ${CMAKE_LIBRARY_OUTPUT_DIRECTORY}/libc++_shared.so)

add_custom_command(
        TARGET Native
        POST_BUILD
        COMMAND
        ${CMAKE_COMMAND} -E copy
        ${PaddleLite_DIR}/cxx/libs/${ANDROID_ABI}/libpaddle_light_api_shared.so
        ${CMAKE_LIBRARY_OUTPUT_DIRECTORY}/libpaddle_light_api_shared.so)

# Export only the JNI methods; OpenCV, TBB and the other static archives stay local.
set(NATIVE_EXPORTS "${CMAKE_CURRENT_LIST_DIR}/Native.map")
set_target_properties(Native PROPERTIES LINK_DEPENDS "${NATIVE_EXPORTS}")
target_link_options(Native PRIVATE
        -Wl,--exclude-libs,ALL
        "-Wl,--version-script=${NATIVE_EXPORTS}"
        -Wl,-z,max-page-size=16384
        -Wl,-z,common-page-size=16384)
