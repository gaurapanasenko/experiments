#!/bin/bash

DIR=$PWD

sudo mksquashfs \
    $DIR/chroot \
    /dev/shm/filesystem.squashfs \
    -comp xz \
    -b 1048576 \
    -e boot
#    -Xcompression-level 9 \

exit 0
