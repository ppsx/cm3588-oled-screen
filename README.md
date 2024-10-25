# cm3588-oled-screen
OLED screen support for CM3588 NAS Kit

## Basic info
It's working on Armbian with a minor tweak to enable I2C. In case of CM3588 NAS Kit, it's I2C-8.

I haven't found a way to enable I2C on any of the official system images (OMV/Debian/Ubuntu). If you know how to do that, please let me know.

The issue with Armbian is that it's installed on SD card and I don't know how to install it on eMMC. Again, if you know how to do that, please let me know :)

To enable I2C in Armbian, I had to:
* create `/boot/overlay-user/` dir if it doesn't exist: `sudo mkdir /boot/overlay-user`
* create `/boot/dtb` symlink if it doesn't exist: `sudo ln -s dtb-<KERNEL_VERSION>-vendor-rk35xx /boot/dtb`; use proper `<KERNEL_VERSION>` here
* copy `/boot/dtb-<KERNEL_VERSION>-vendor-rk35xx/rockchip/overlay/rk3588-i2c8-m2.dtbo` to `/boot/overlay-user/` to make it "visible" by the config: `sudo cp /boot/dtb/rockchip/overlay/rk3588-i2c8-m2.dtbo /boot/overlay-user/`
* add `user_overlays=rk3588-i2c8-m2` to `/boot/armbianEnv.txt`

My `/boot/armbianEnv.txt` looks like this:
```
verbosity=1
bootlogo=false
overlay_prefix=rockchip-rk3588
fdtfile=rockchip/rk3588-nanopc-cm3588-nas.dtb
rootdev=UUID=324c17d1-5084-4be1-a1d6-5952caea5aee
rootfstype=ext4
user_overlays=rk3588-i2c8-m2
usbstoragequirks=0x2537:0x1066:u,0x2537:0x1068:u
```

Once system is rebooted, the I2C-8 should be accessible.

## Installation
There's no installation script yet, sorry ;)

You need to work as root.

Clone this repo to `/opt/oled-screen/` directory: `cd /opt && git clone https://github.com/ppsx/cm3588-oled-screen oled-screen`

Get into the dir: `cd oled-screen`

Create Python's venv: `python -m venv venv`

Activate it: `source venv/bin/activate`

Install dependencies: `pip install -r requirements.txt`

Copy `*.service` file to systemd dir: `cp oled-screen.service /etc/systemd/system/`

Reload systemd: `systemctl daemon-reload`

Start the service: `systemctl start oled-screen`

If everything is ok, the service has to be enabled to start after booting: `systemctl enable oled-screen`
That's it.

## More info
When system is booting and oled-screen service is started, it shows nice boot logo animation. Then `System ready` is printed.
The "User button" is used to switch between different "pages". Each page contains some basic info about: CPU utilization (CPU), memory and swap (MEM), disk (system disk and NVMe) and network (eth0).
After one minute of inactivity the screen is turned off. User button brings it back to the first page (CPU).

## Preview


https://github.com/ppsx/cm3588-oled-screen/assets/7107135/b9ce4e7e-c01b-41d1-a84b-af80d4e42d62

