#!/bin/bash

rm /home/user/Programs/zfs_qat_test/csd_mountpoint/*
sudo zfs unmount -f mypool/myfs
sudo zfs destroy mypool/myfs
sudo zpool destroy mypool



cp /home/user/Programs/zfs_qat_test/silesia.tar /home/user/Programs/zfs_qat_test/csd_mountpoint/
