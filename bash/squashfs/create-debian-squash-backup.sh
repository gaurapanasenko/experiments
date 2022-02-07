#!/bin/bash

DIR=$PWD

rm -rf $DIR/{scratch,image,debian-gaura.iso}
#rm -rf $DIR/{scratch,debian-custom.iso}

mkdir -p $DIR/{scratch,image/live}

sudo mksquashfs \
    $DIR/chroot \
    $DIR/image/live/filesystem.squashfs \
    -e boot \
    -e /etc/fstab \
    -e /home/.ecryptfs \
    -e /home/egor \
    -e srv

sudo mksquashfs \
    $DIR/chroot/etc/skel \
    $DIR/image/skel.squashfs \

cp $DIR/chroot/boot/vmlinuz-* \
    $DIR/image/vmlinuz && \
cp $DIR/chroot/boot/initrd.img-* \
    $DIR/image/initrd

cat <<'EOF' >$DIR/scratch/grub.cfg

search --set=root --file /Debian_S46sdjMVqs

insmod all_video

set default="0"
set timeout=30

menuentry "Debian Gaura Live" {
    linux /vmlinuz boot=live quiet
    initrd /initrd
}
#menuentry "Debian Gaura Live to RAM" {
#    linux /vmlinuz boot=live quiet nomodeset toram
#    initrd /initrd
#}
menuentry "Debian Gaura Live persistence" {
    linux /vmlinuz boot=live quiet persistence
    initrd /initrd
}
EOF

touch $DIR/image/Debian_S46sdjMVqs

grub-mkstandalone \
    --format=i386-pc \
    --output=$DIR/scratch/core.img \
    --install-modules="linux normal iso9660 biosdisk memdisk search tar ls" \
    --modules="linux normal iso9660 biosdisk search" \
    --locales="" \
    --fonts="" \
    "boot/grub/grub.cfg=$DIR/scratch/grub.cfg"


cat \
    /usr/lib/grub/i386-pc/cdboot.img \
    $DIR/scratch/core.img \
> $DIR/scratch/bios.img

exit 0

xorriso \
    -as mkisofs \
    -iso-level 3 \
    -full-iso9660-filenames \
    -volid "Debian_S46sdjMVqs" \
    --grub2-boot-info \
    --grub2-mbr /usr/lib/grub/i386-pc/boot_hybrid.img \
    -eltorito-boot \
        boot/grub/bios.img \
        -no-emul-boot \
        -boot-load-size 4 \
        -boot-info-table \
        --eltorito-catalog boot/grub/boot.cat \
    -output "$DIR/debian-gaura.iso" \
    -graft-points \
        "$DIR/image" \
        /boot/grub/bios.img=$DIR/scratch/bios.img

chmod 644 $DIR/debian-gaura.iso

exit 0
