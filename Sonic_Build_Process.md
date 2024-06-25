# Build SONiC Switch Images

# Hardware

* Multiple cores to increase build speed
* Plenty of RAM (less than 8 GiB is likely to cause issues)
* 300G of free disk space
* KVM Virtualization Support.

# Environment

* OS = Ubuntu 22.04 or later 
* Device = Accton_as7326_56x
* RAM = 16GB
* Storage = 300GB+ SSD
* CPU Core = 4x CPU cores


# Dependencies/Prerequisites

1. To install maven and jdk
    sudo apt update
    sudo apt install maven
    sudo apt install openjdk-11-jdk-headless
    Check for the version use
    java --version
    mvn –version







make init

make configure PLATFORM=broadcom

Add dsserve to /target/files/bullseye/dsserve

make target/sonic-broadcom.bin


if you recived error like "Http + Docker"

    Find below Line in build_debian.sh
    sudo https_proxy=$https_proxy LANG=C chroot $FILESYSTEM_ROOT pip3 install 'docker==6.1.1'
    Replace it with below line 
    sudo https_proxy=$https_proxy LANG=C chroot $FILESYSTEM_ROOT pip3 install 'requests<2.32.0'


