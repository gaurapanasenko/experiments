#!/bin/sh

set -e

BIN_DIR="`dirname -- $0`"
BIN_DIR=`realpath "$BIN_DIR"`
SOURCE_PATH="$BIN_DIR"

source "${BIN_DIR}/enviroment.sh"

CMAKE="${QT_HOME}/Tools/CMake/bin/cmake"

create_build_path() {
    BUILD_PATH=`realpath "$SOURCE_PATH/build_${BUILD_ARCH}"`
}

build_one() {
    BUILD_ARCH=$1
    QT_BUILD_ARCH=$2
    QTDIR=${QTPREFIX}/android_${QT_BUILD_ARCH}
    BUILD_PATH=`realpath "$SOURCE_PATH/build_${BUILD_ARCH}"`

    mkdir -p "$BUILD_PATH"
    $CMAKE \
     -S "${SOURCE_PATH}" \
     -B "${BUILD_PATH}" \
     -DCMAKE_GENERATOR:STRING=Ninja \
     -DCMAKE_BUILD_TYPE:STRING=Debug \
     -DCMAKE_PREFIX_PATH:PATH="${QTDIR}" \
     -DCMAKE_FIND_ROOT_PATH:PATH="${QTDIR}" \
     -DANDROID_NDK:PATH="${ANDROID_NDK_ROOT}" \
     -DANDROID_ABI:STRING=${BUILD_ARCH} \
     -DANDROID_SDK_ROOT:PATH="${ANDROID_SDK_ROOT}" \
     -DANDROID_PLATFORM:STRING="${ANDROID_NDK_PLATFORM}" \
     -DCMAKE_TOOLCHAIN_FILE:FILEPATH="${ANDROID_NDK_ROOT}/build/cmake/android.toolchain.cmake" \

    $CMAKE --build "${BUILD_PATH}"
}

build_one arm64-v8a arm64_v8a
build_one armeabi-v7a armv7
