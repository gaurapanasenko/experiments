# GStreamer QML6 Plugin Test on Android and Desktop

This project contains an experimental program to test the GStreamer QML6 plugin on Android and Desktop platforms. The experiment works correctly and was tested with Qt version 6.8.3.

## Prepare

Download GStreamer prebuilt package:
https://gstreamer.freedesktop.org/data/pkg/android/1.26.0/gstreamer-1.0-android-universal-1.26.0.tar.xz

Inside each ABI directory, especially `armv7`, find the file `share/cmake/FindGStreamerMobile.cmake` and remove the following line (line 106):

```cmake
set(NEEDS_NOTEXT_FIX TRUE)
```

Android does not support text relocations in newer versions, so this line must be removed to avoid runtime errors.

## Build Instructions (Linux)

1. Copy `enviroment.sh.example` to `enviroment.sh`.
2. Edit `enviroment.sh` and set correct paths:

```sh
export JAVA_HOME=/usr/lib64/jvm/java-17-openjdk
export ANDROID_HOME=/path/to/android
export QT_HOME=/path/to/qt
export QT_VERSION=6.8.3
export GSTREAMER_ROOT_ANDROID=/path/to/gstreamer
```

- `JAVA_HOME`: path to Java 17
- `ANDROID_HOME`: path to Android SDK
- `QT_HOME`: path to Qt for Android
- `QT_VERSION`: set to 6.8.3
- `GSTREAMER_ROOT_ANDROID`: path to unpacked GStreamer prebuilt directory

3. Run the build script:

```sh
./build.sh
```

