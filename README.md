# cm3588-oled-screen
OLED screen support for CM3588 NAS Kit

## Basic info
It's working on Armbian with a minor tweak to enable I2C. In case of CM3588 NAS Kit, it's I2C-8.

I haven't found a way to enable I2C on any of the official system images (OMV/Debian/Ubuntu). If you know how to do that, please let me know.

The issue with Armbian is that it's installed on SD card and I don't know how to install it on eMMC. Again, if you know how to do that, please let me know :)

To enable I2C in Armbian, I had to:
* make copy of `/boot/dtb-6.1.43-vendor-rk35xx/rockchip/overlay/rk3588-i2c8-m2.dtbo` as `/boot/dtb-6.1.43-vendor-rk35xx/rockchip/overlay/rockchip-rk3588-i2c
8-m2.dtbo` to make it "visible" by the config
* add `overlays=i2c8-m2` to `/boot/armbianEnv.txt`

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

