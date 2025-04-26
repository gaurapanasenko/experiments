cmake_minimum_required(VERSION 3.16)

project(gstreamer-androqt VERSION 0.1 LANGUAGES C CXX)

set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)

if (ANDROID)
  set(CMAKE_POSITION_INDEPENDENT_CODE ON)
  if(DEFINED ENV{GSTREAMER_ROOT_ANDROID})
    set(GSTREAMER_ROOT_ANDROID $ENV{GSTREAMER_ROOT_ANDROID})
  endif()

  if(NOT DEFINED GSTREAMER_ROOT_ANDROID)
      message(FATAL_ERROR "GSTREAMER_ROOT_ANDROID is not defined!")
  endif()

  if(ANDROID_ABI STREQUAL "armeabi")
      set(GSTREAMER_ROOT_ABI "${GSTREAMER_ROOT_ANDROID}/arm")
  elseif(ANDROID_ABI STREQUAL "armeabi-v7a")
      set(GSTREAMER_ROOT_ABI "${GSTREAMER_ROOT_ANDROID}/armv7")
  elseif(ANDROID_ABI STREQUAL "arm64-v8a")
      set(GSTREAMER_ROOT_ABI "${GSTREAMER_ROOT_ANDROID}/arm64")
  elseif(ANDROID_ABI STREQUAL "x86")
      set(GSTREAMER_ROOT_ABI "${GSTREAMER_ROOT_ANDROID}/x86")
  elseif(ANDROID_ABI STREQUAL "x86_64")
      set(GSTREAMER_ROOT_ABI "${GSTREAMER_ROOT_ANDROID}/x86_64")
  else()
      message(FATAL_ERROR "Target arch ABI not supported: ${ANDROID_ABI}")
  endif()
  list(APPEND CMAKE_MODULE_PATH "${GSTREAMER_ROOT_ABI}/share/cmake")

  set(GSTREAMER_NDK_BUILD_PATH  "${GSTREAMER_ROOT_ABI}/share/gst-android/ndk-build/")
  include("${GSTREAMER_NDK_BUILD_PATH}/plugins.cmake")
  set(GSTREAMER_PLUGINS
      ${GSTREAMER_PLUGINS_CORE}
      # ${GSTREAMER_PLUGINS_PLAYBACK}
      # ${GSTREAMER_PLUGINS_CODECS}
      # ${GSTREAMER_PLUGINS_NET}
      ${GSTREAMER_PLUGINS_SYS}
      autodetect videoconvertscale videotestsrc
      playback androidmedia soup isomp4 fmp4 mp4 mpg123 videoparsersbad vpx matroska openh264)
  set(GStreamer_EXTRA_DEPS gstreamer-video-1.0)

  find_package(GStreamerMobile COMPONENTS ${GSTREAMER_PLUGINS} fonts REQUIRED)

  find_library(ANDROID_LIB android REQUIRED)

  set(target_libs GStreamer::mobile ${ANDROID_LIB} ${_gst_gstqml6})
else()
  include(FindPkgConfig)
  if(!${PKG_CONFIG_FOUND})
    MESSAGE(FATAL_ERROR "pkg-config required. Please install it")
    return ("Error - pkg-config not found")
  endif()

  pkg_check_modules(GSTREAMER gstreamer-1.0>=1.6 gstreamer-video-1.0>=1.6 REQUIRED)
  link_directories(${GSTREAMER_LIBRARY_DIRS})
  include_directories(${GSTREAMER_INCLUDE_DIRS})
  set(target_libs ${GSTREAMER_LIBRARIES})
endif()

find_package(Qt6 REQUIRED COMPONENTS Core Gui Qml Quick ShaderTools)


if (ANDROID)
    target_link_libraries(GStreamerMobile
        PRIVATE Qt6::Quick
    )
endif()

#add_subdirectory(gstqml6)

qt_standard_project_setup(REQUIRES 6.5)


set(android_files
  android/AndroidManifest.xml
  android/build.gradle
  android/java/org/freedesktop/gstreamer/GStreamer.java
  android/java/top/elfiny/GstActivity.java
  android/java/top/elfiny/GstPlayer.java
  android/java/top/elfiny/GstSurfaceView.java
)

qt_add_executable(appgstreamer-androqt main.cpp ${android_files})

qt_add_qml_module(appgstreamer-androqt
    URI gstreamer
    VERSION 1.0
    QML_FILES
        Main.qml
    SOURCES
      gstplayer.h gstplayer.cpp
      gstplayerfactory.h gstplayerfactory.cpp
)

#qt6_add_shaders(appgstreamer-androqt "gstqml6_shaders"
#    GLSL "100 es,120,330"
#    BATCHABLE
#    PREFIX
#        "/org/freedesktop/gstreamer/qml6"
#    FILES
#        RGBA.frag vertex.vert
#)

# qt_add_resources(appgstreamer-androqt "videos"
#     PREFIX "/"
#     FILES
#         test.mp4)

# Qt for iOS sets MACOSX_BUNDLE_GUI_IDENTIFIER automatically since Qt 6.1.
# If you are developing for iOS or macOS you should consider setting an
# explicit, fixed bundle identifier manually though.
set_target_properties(appgstreamer-androqt PROPERTIES
#    MACOSX_BUNDLE_GUI_IDENTIFIER com.example.appgstreamer-androqt
    MACOSX_BUNDLE_BUNDLE_VERSION ${PROJECT_VERSION}
    MACOSX_BUNDLE_SHORT_VERSION_STRING ${PROJECT_VERSION_MAJOR}.${PROJECT_VERSION_MINOR}
    MACOSX_BUNDLE TRUE
    WIN32_EXECUTABLE TRUE
    QT_ANDROID_PACKAGE_SOURCE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/android"
    QT_ANDROID_EXTRA_LIBS "${ANDROID_EXTRA_LIBS}"
)

target_link_libraries(appgstreamer-androqt
    PRIVATE Qt6::Quick ${target_libs}
)

include(GNUInstallDirs)
install(TARGETS appgstreamer-androqt
    BUNDLE DESTINATION .
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
)
