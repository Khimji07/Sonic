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

# Faced Issue During Build Time

## 1) Build sonic-broadcom.bin via make target/sonic-broadcom.bin command. But I get below error on building docker-gbsyncd-broncos:

```shell
Step 22/32 : COPY ["files/dsserve", "/usr/bin/"]
COPY failed: file not found in build context or excluded by .dockerignore: stat files/dsserve: file does not exist
```

### Solution

I download dsserve from this [link](https://github.com/Khimji07/Sonic/blob/main/dsserve) manually and add it to
`sonic-buildimage/target/files/bullseye/`

#### Note : When you build the image using bullseye so you encountered this error. 

## 2) Docker client failing to connect : requests.exceptions.InvalidURL: Not supported URL scheme http+docker

* Running Docker inside chroot results in "requests.exceptions.InvalidURL: Not supported URL scheme http+docker" due to Docker client failing to connect to Docker daemon.

`requests.exceptions.InvalidURL: Not supported URL scheme http+docker`

### Solution

Add pip install requests package and pin version to <2.32.0 in build_debian.sh

```bash
# Find below Line in build_debian.sh
sudo https_proxy=$https_proxy LANG=C chroot $FILESYSTEM_ROOT pip3 install 'docker==6.1.1'
# Replace it with below line 
sudo https_proxy=$https_proxy LANG=C chroot $FILESYSTEM_ROOT pip3 install 'requests<2.32.0'
```

#### Note: During the build time do not use the package manager for any other task because may be it's cause the issue.


## 3) In the bootlog we received PDDF_ERROR for LED status. `PDDF_ERROR: dev_operation: Invalid value for dev_ops STATUS_LED_COLOR`

ERROR : 

```bash
[   43.895169] PDDF_ERROR: dev_operation: Invalid value for dev_ops STATUS_LED_COLOR_BLUE_BLINK
[   43.911763] PDDF_ERROR: dev_operation: Invalid value for dev_ops STATUS_LED_COLOR_GREEN_BLINK
[   43.928367] PDDF_ERROR: dev_operation: Invali3) In the bootlog we received PDDF_ERROR for LED status. PDDF_ERROR: dev_operation: Invalid value for dev_ops STATUS_LED_COLORd value for dev_ops STATUS_LED_COLOR_AMBER_BLINK
[   43.944995] PDDF_ERROR: dev_operation: Invalid value for dev_ops STATUS_LED_COLOR_BLUE
[   43.960874] PDDF_ERROR: dev_operation: Invalid value for dev_ops STATUS_LED_COLOR_GREEN
[   43.976833] PDDF_ERROR: dev_operation: Invalid value for dev_ops STATUS_LED_COLOR_AMBER
[   43.992871] PDDF_ERROR: dev_operation: Invalid value for dev_ops STATUS_LED_COLOR_OFF
[   44.009082] PDDF_ERROR: dev_operation: Invalid value for dev_ops STATUS_LED_COLOR_BLUE_BLINK
[   44.025958] PDDF_ERROR: dev_operation: Invalid value for dev_ops STATUS_LED_COLOR_GREEN_BLINK
[   44.043110] PDDF_ERROR: dev_operation: Invalid value for dev_ops STATUS_LED_COLOR_AMBER_BLINK
[   44.059224] PDDF_ERROR: dev_operation: Invalid value for dev_ops STATUS_LED_COLOR_BLUE
[   44.075284] PDDF_ERROR: dev_operation: Invalid value for dev_ops STATUS_LED_COLOR_GREEN
[   44.091797] PDDF_ERROR: dev_operation: Invalid value for dev_ops STATUS_LED_COLOR_AMBER
[   44.108294] PDDF_ERROR: dev_operation: Invalid value for dev_ops STATUS_LED_COLOR_OFF
```

Device Boot Logs :

```bash
Loading SONiC-OS OS kernel ...Loading SONiC-OS OS kernel ...

Loading SONiC-OS OS initial ramdisk ...Loading SONiC-OS OS initial ramdisk ...

tune2fs 1.47.0 (5-Feb-2023)
Setting reserved blocks percentage to 0% (0 blocks)
Setting reserved blocks count to 0
[    6.181045] kdump-tools[704]: Starting kdump-tools:
[    6.200355] kdump-tools[708]: no crashkernel= parameter in the kernel cmdline ... failed!
[    6.224000] rc.local[743]: + grep build_version
[FAILED] Failed to start nginx.serv…server and a reverse proxy server.
[    6.242894] rc.local[742]: + cat /etc/sonic/sonic_version.yml
[    6.277931] rc.local[744]: + sed -e s/build_version: //g;s/'//g
[    6.297610] rc.local[737]: + SONIC_VERSION=main.0-dirty-20240605.145553
[    6.312193] rc.local[737]: + FIRST_BOOT_FILE=/host/image-main.0-dirty-20240605.145553/platform/firsttime
[    6.333067] rc.local[737]: + SONIC_CONFIG_DIR=/host/image-main.0-dirty-20240605.145553/sonic-config
[    6.352228] rc.local[737]: + SONIC_ENV_FILE=/host/image-main.0-dirty-20240605.145553/sonic-config/sonic-environment
[    6.372201] rc.local[737]: + [ -d /host/image-main.0-dirty-20240605.145553/sonic-config -a -f /host/image-main.0-dirty-20240605.145553/sonic-config/sonic-environment ]
[    6.396146] rc.local[737]: + logger SONiC version main.0-dirty-20240605.145553 starting up...
[    6.416154] rc.local[737]: + grub_installation_needed=
[    6.432145] rc.local[737]: + [ ! -e /host/machine.conf ]
[    6.448125] rc.local[737]: + . /host/machine.conf
[    6.464124] rc.local[737]: + onie_arch=x86_64
[    6.484162] rc.local[737]: + onie_bin=
[    6.496125] rc.local[737]: + onie_boot_reason=rescue
[    6.516123] rc.local[737]: + onie_build_date=2020-11-16T10:42+08:00
[    6.536088] rc.local[737]: + onie_build_machine=accton_as7326_56x
[    6.552203] rc.local[737]: + onie_build_platform=x86_64-accton_as7326_56x-r0
[    6.568116] rc.local[737]: + onie_cli_static_parms=
[    6.584103] rc.local[737]: + onie_cli_static_url=tftp://172.16.100.10/sonic-broadcom.bin
[    6.604080] rc.local[737]: + onie_config_version=1
[    6.624076] rc.local[737]: + onie_dev=/dev/sda2
[    6.640058] rc.local[737]: + onie_exec_url=tftp://172.16.100.10/sonic-broadcom.bin
[    6.660054] rc.local[737]: + onie_firmware=auto
[    6.676051] rc.local[737]: + onie_grub_image_name=grubx64.efi
[    6.692052] rc.local[737]: + onie_initrd_tmp=/
[    6.708063] rc.local[737]: + onie_installer=/var/tmp/installer
[    6.724064] rc.local[737]: + onie_kernel_version=4.9.95
[    6.740123] rc.local[737]: + onie_machine=accton_as7326_56x
[    6.756115] rc.local[737]: + onie_machine_rev=0
[    6.772121] rc.local[737]: + onie_partition_type=gpt
[    6.788145] rc.local[737]: + onie_platform=x86_64-accton_as7326_56x-r0
[    6.804178] rc.local[737]: + onie_root_dir=/mnt/onie-boot/onie
[    6.820181] rc.local[737]: + onie_skip_ethmgmt_macs=no
[    6.836189] rc.local[737]: + onie_switch_asic=bcm
[    6.852137] rc.local[737]: + onie_uefi_arch=x64
[    6.868153] rc.local[737]: + onie_uefi_boot_loader=grubx64.efi
[    6.884164] rc.local[737]: + onie_vendor_id=259
[    6.904113] rc.local[737]: + onie_version=2020.08.00.02
[    6.920099] rc.local[737]: + program_console_speed
[    6.937890] rc.local[758]: + cat /proc/cmdline
[    6.953646] rc.local[761]: + cut -d , -f2
[    6.969551] rc.local[759]: + grep -Eo console=tty(S|AMA)[0-9]+,[0-9]+
[    6.985745] rc.local[737]: + speed=115200
[    7.000138] rc.local[737]: + [ -z 115200 ]
[    7.012144] rc.local[737]: + CONSOLE_SPEED=115200
[    7.028858] rc.local[766]: + grep keep-baud
[    7.044598] rc.local[765]: + grep agetty /lib/systemd/system/serial-getty@.service
[    7.064380] rc.local[766]: ExecStart=-/sbin/agetty -o '-p -- \\u' --keep-baud 115200,57600,38400,9600 - $TERM
[    7.084576] rc.local[737]: + [ 0 = 0 ]
[    7.096179] rc.local[737]: + sed -i s|\-\-keep\-baud .* %I| 115200 %I|g /lib/systemd/system/serial-getty@.service
[    7.116115] rc.local[737]: + systemctl daemon-reload
[    7.132072] rc.local[737]: + [ -f /host/image-main.0-dirty-20240605.145553/platform/firsttime ]
[    7.152226] rc.local[737]: + echo First boot detected. Performing first boot tasks...
[    7.172161] rc.local[737]: First boot detected. Performing first boot tasks...
[    7.188141] rc.local[737]: + [ -n  ]
[    7.200251] rc.local[737]: + [ -n x86_64-accton_as7326_56x-r0 ]
[    7.216171] rc.local[737]: + platform=x86_64-accton_as7326_56x-r0
[    7.232116] rc.local[737]: + [ -d /host/old_config ]
[    7.248130] rc.local[737]: + [ -f /host/minigraph.xml ]
[    7.264147] rc.local[737]: + [ -n  ]
[    7.276153] rc.local[737]: + touch /tmp/pending_config_initialization
[    7.292120] rc.local[737]: + touch /tmp/notify_firstboot_to_platform
[    7.308598] rc.local[737]: + [ ! -d /host/reboot-cause/platform ]
[    7.324118] rc.local[737]: + mkdir -p /host/reboot-cause/platform
[    7.340112] rc.local[737]: + [ -d /host/image-main.0-dirty-20240605.145553/platform/x86_64-accton_as7326_56x-r0 ]
[    7.360134] rc.local[737]: + [ -f /host/image-main.0-dirty-20240605.145553/platform/common/Packages.gz ]
[    7.380136] rc.local[737]: + mv /etc/apt/sources.list /etc/apt/sources.list.rc-local
[    7.396120] rc.local[737]: + echo deb [trusted=yes] file:///host/image-main.0-dirty-20240605.145553/platform/common /
[    7.416129] rc.local[737]: + LANG=C DEBIAN_FRONTEND=noninteractive apt-get -o Acquire::Retries=1 update
[    7.437355] rc.local[833]: Get:1 file:/host/image-main.0-dirty-20240605.145553/platform/common  InRelease
[    7.456154] rc.local[833]: Ign:1 file:/host/image-main.0-dirty-20240605.145553/platform/common  InRelease
[    7.480178] rc.local[833]: Get:2 file:/host/image-main.0-dirty-20240605.145553/platform/common  Release
[    7.504137] rc.local[833]: Ign:2 file:/host/image-main.0-dirty-20240605.145553/platform/common  Release
[    7.524132] rc.local[833]: Get:3 file:/host/image-main.0-dirty-20240605.145553/platform/common  Packages [6696 B]
[    7.544132] rc.local[833]: Ign:4 https://download.docker.com/linux/debian bookworm InRelease
[    7.880900] rc.local[833]: Err:4 https://download.docker.com/linux/debian bookworm InRelease
[    7.900142] rc.local[833]:   Temporary failure resolving 'download.docker.com'
[    7.920145] rc.local[833]: Reading package lists...
[    7.940115] rc.local[833]: W: Failed to fetch https://download.docker.com/linux/debian/dists/bookworm/InRelease  Temporary failure resolving 'download.docker.com'
[    7.968095] rc.local[833]: W: Some index files failed to download. They have been ignored, or old ones used instead.
[    7.988154] rc.local[737]: + LANG=C DEBIAN_FRONTEND=noninteractive apt-get -o DPkg::Path=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/bin -y install /host/imagb
[    8.072206] rc.local[904]: Reading package lists...
[    8.088206] rc.local[904]: Building dependency tree...
[    8.104166] rc.local[904]: Reading state information...
[    8.120174] rc.local[904]: The following NEW packages will be installed:
[    8.136143] rc.local[904]:   sonic-platform-accton-as7326-56x
[    8.152197] rc.local[904]: 0 upgraded, 1 newly installed, 0 to remove and 0 not upgraded.
[    8.172187] rc.local[904]: Need to get 0 B/373 kB of archives.
[    8.188165] rc.local[904]: After this operation, 2956 kB of additional disk space will be used.
[    8.208151] rc.local[904]: Get:1 file:/host/image-main.0-dirty-20240605.145553/platform/common  sonic-platform-accton-as7326-56x 1.1 [373 kB]
[   33.220720] rc.local[912]: debconf: delaying package configuration, since apt-utils is not installed
[   33.284346] rc.local[904]: Selecting previously unselected package sonic-platform-accton-as7326-56x.
(Reading database ... 44353 files and directories currently installed.)
[   33.948501] rc.local[904]: Preparing to unpack .../sonic-platform-accton-as7326-56x_1.1_amd64.deb ...
[   33.968199] rc.local[904]: Unpacking sonic-platform-accton-as7326-56x (1.1) ...
[   34.442426] rc.local[904]: Setting up sonic-platform-accton-as7326-56x (1.1) ...
[   38.791981] rc.local[904]: Created symlink /etc/systemd/system/multi-user.target.wants/pddf-platform-init.service -> /lib/systemd/system/pddf-platform-init.service.
[   43.895169] PDDF_ERROR: dev_operation: Invalid value for dev_ops STATUS_LED_COLOR_BLUE_BLINK
[   43.911763] PDDF_ERROR: dev_operation: Invalid value for dev_ops STATUS_LED_COLOR_GREEN_BLINK
[   43.928367] PDDF_ERROR: dev_operation: Invalid value for dev_ops STATUS_LED_COLOR_AMBER_BLINK
[   43.944995] PDDF_ERROR: dev_operation: Invalid value for dev_ops STATUS_LED_COLOR_BLUE
[   43.960874] PDDF_ERROR: dev_operation: Invalid value for dev_ops STATUS_LED_COLOR_GREEN
[   43.976833] PDDF_ERROR: dev_operation: Invalid value for dev_ops STATUS_LED_COLOR_AMBER
[   43.992871] PDDF_ERROR: dev_operation: Invalid value for dev_ops STATUS_LED_COLOR_OFF
[   44.009082] PDDF_ERROR: dev_operation: Invalid value for dev_ops STATUS_LED_COLOR_BLUE_BLINK
[   44.025958] PDDF_ERROR: dev_operation: Invalid value for dev_ops STATUS_LED_COLOR_GREEN_BLINK
[   44.043110] PDDF_ERROR: dev_operation: Invalid value for dev_ops STATUS_LED_COLOR_AMBER_BLINK
[   44.059224] PDDF_ERROR: dev_operation: Invalid value for dev_ops STATUS_LED_COLOR_BLUE
[   44.075284] PDDF_ERROR: dev_operation: Invalid value for dev_ops STATUS_LED_COLOR_GREEN
[   44.091797] PDDF_ERROR: dev_operation: Invalid value for dev_ops STATUS_LED_COLOR_AMBER
[   44.108294] PDDF_ERROR: dev_operation: Invalid value for dev_ops STATUS_LED_COLOR_OFF
[   47.714660] rc.local[737]: + rm -f /etc/apt/sources.list.d/sonic_debian_extension.list
[   47.732186] rc.local[737]: + rm -f /var/lib/apt/lists/_host_image-main.0-dirty-20240605.145553_platform_common_Packages.lz4
[   47.752114] rc.local[737]: + mv /etc/apt/sources.list.rc-local /etc/apt/sources.list
[   47.768126] rc.local[737]: + sync
[   47.780156] rc.local[737]: + [ -n x86_64-accton_as7326_56x-r0 ]
[   47.796133] rc.local[737]: + [ -n  ]
[   47.808092] rc.local[737]: + mkdir -p /var/platform
[   47.824258] rc.local[737]: + [ -f /etc/default/kdump-tools ]
[   47.840201] rc.local[737]: + sed -i -e s/_PLATFORM_/x86_64-accton_as7326_56x-r0/g /etc/default/kdump-tools
[   47.860195] rc.local[737]: + firsttime_exit
[   47.872183] rc.local[737]: + rm -rf /host/image-main.0-dirty-20240605.145553/platform/firsttime
[   47.892194] rc.local[737]: + exit 0
[FAILED] Failed to start determine-…eboot cause determination service.
```

### Solution

Download the "pddf-device.json" from this [link](https://github.com/Khimji07/Sonic/blob/main/device/accton/x86_64-accton_as7326_56x-r0/pddf/pddf-device.json) and replace it to `sonic-buildimage/device/accton/x86_64-accton_as7326_56x-r0/pddf/pddf-device.json`

#### Note : I Enhanced the LED attributes name in this file.