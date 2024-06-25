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
```shell
sudo apt update
sudo apt install maven
sudo apt install openjdk-11-jdk-headless
```
* Check for the version use
```shell
java --version
mvn --version
```

2. Install curl using
```shell
sudo apt install curl
```
* To check for the version use
```shell
curl --version
```

3. Install zip and unzip using
```shell
sudo apt install zip
sudo apt install unzip
```
* To check for the version use
```shell
zip -v
unzip -v
```

4. Install python using
```shell
sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3
```
* To check for the version use
```shell
python3 --version
```

5. Install pip
```shell
sudo apt install python3-pip
```
* To check for the version use
```shell
pip --version
```

6. Install enum34
```shell
pip install enum34
```

7. Install jinja2 and j2cli using
```shell
pip3 install jinja2
pip install j2cli
```
or
```shell
sudo apt-get install j2cli
```
* To check for the version and details
```shell
pip3 show jinja2
pip3 show j2cli
```

8. Install Docker using 
* Install [Docker](https://docs.docker.com/engine/install/) and configure your system to allow running the 'docker' command without 'sudo':
* Add current user to the docker group: `sudo gpasswd -a ${USER} docker`
* Log out and log back in so that your group membership is re-evaluated
* If you are using Linux kernel 5.3 or newer, then you must use Docker 20.10.10 or newer. This is because older Docker versions did not allow the `clone3` syscall, which is now used in Bookworm.

# Clone the repository with all the git submodules

To clone the code repository recursively:

```shell
git clone --recurse-submodules https://github.com/sonic-net/sonic-buildimage.git
```

# Building the Image

To build SONiC installer image and docker images, run the following commands:

* Ensure the 'overlay' module is loaded on your development system
```shell
sudo modprobe overlay
```

* Enter the source directory
```shell
cd sonic-buildimage
```

* (Optional) Checkout a specific branch. By default, it uses master branch. For example, to checkout the branch 202405, use "git checkout 202405"
```shell
# We used a default branch "master"
git checkout [branch_name]
```

* Execute make init once after cloning the repo, or after fetching remote repo with submodule updates
```shell
make init
```

* Execute make configure once to configure ASIC

```shell
make configure PLATFORM=[ASIC_VENDOR]
```

    The supported ASIC vendors are:

    * PLATFORM=barefoot
    * PLATFORM=broadcom
    * PLATFORM=marvell
    * PLATFORM=mellanox
    * PLATFORM=cavium
    * PLATFORM=centec
    * PLATFORM=nephos
    * PLATFORM=nvidia-bluefield
    * PLATFORM=innovium
    * PLATFORM=vs

```shell
# We have broadcome device so we are used the specific broadcom plateform
make configure PLATFORM=broadcom
```

* The SONiC installer contains all docker images needed.
* SONiC uses one image for all devices of a same ASIC vendor.
* For Broadcom ASIC, we build ONIE and EOS image.
* EOS image is used for Arista devices,
* ONIE image is used for all other Broadcom ASIC based devices.

```shell
make configure PLATFORM=broadcom
# build debian stretch required targets
BLDENV=stretch make stretch
# build ONIE image
make target/sonic-broadcom.bin
# build EOS image
make target/sonic-aboot-broadcom.swi
```

# Facing Issue During Build

## Build sonic-broadcom.bin via make target/sonic-broadcom.bin command. But I get below error on building docker-gbsyncd-broncos:

```shell
Step 22/32 : COPY ["files/dsserve", "/usr/bin/"]
COPY failed: file not found in build context or excluded by .dockerignore: stat files/dsserve: file does not exist
```


Add dsserve to /target/files/bullseye/dsserve

make target/sonic-broadcom.bin


if you recived error like "Http + Docker"

    Find below Line in build_debian.sh
    sudo https_proxy=$https_proxy LANG=C chroot $FILESYSTEM_ROOT pip3 install 'docker==6.1.1'
    Replace it with below line 
    sudo https_proxy=$https_proxy LANG=C chroot $FILESYSTEM_ROOT pip3 install 'requests<2.32.0'


