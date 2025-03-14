# Raspberry PI 5 honey dispenser

## Install
This script will automatically:
- apply patch for Raspberry PI 5,
- install dependencies,
- create desktop and menu entry and start the application

```console
pi@raspberrypi:~ $ git clone --depth=1 https://github.com/mstumberger/raspi5_honey_dispenser.git honey_dispenser
pi@raspberrypi:~ $ cd honey_dispenser
pi@raspberrypi:~/honey_dispenser $ chmod +x install_and_start.sh
pi@raspberrypi:~/honey_dispenser $ ./install_and_start.sh
```

## Manual Install

- Set rpi to performance mode:

```console
    echo performance | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor
```

- [lgpio-dev](http://abyz.me.uk/lg/index.html) is required to be installed. It may be available to you via apt:

```console
sudo apt-get install -y liblgpio-dev
```
If it is not available, manually build and install it by following the instructions [here](https://abyz.me.uk/lg/download.html#Download&Install).

- Install C++ dependency for python library

```console
pi@raspberrypi:~ $ git clone --depth=1 https://github.com/endail/hx711
pi@raspberrypi:~ $ cd hx711
```

For RPi 5 the expansion header GPIO pins are now on /dev/gpiochip4 instead of /dev/gpiochip0. [endail/hx711/issues/85](https://github.com/endail/hx711/issues/85#issuecomment-2129032985)

```console
pi@raspberrypi:~/hx711 $ cd src
pi@raspberrypi:~/hx711/src $ sed -i 's/Utility::openGpioHandle(0)/Utility::openGpioHandle(4)/g' HX711.cpp
pi@raspberrypi:~/hx711/src $ cd ..
```

```console
pi@raspberrypi:~/hx711 $ make && sudo make install
```

Source: [Raspberry Pi HX711 C++ Library Readme](https://github.com/endail/hx711/blob/master/README.md)

- clone application create virtual environment and install python dependencies

```console
pi@raspberrypi:~ $ git clone --depth=1 https://github.com/mstumberger/raspi5_honey_dispenser.git honey_dispenser
pi@raspberrypi:~ $ cd honey_dispenser
pi@raspberrypi:~/honey_dispenser $ python3 -m venv venv
pi@raspberrypi:~/honey_dispenser $ source venv/bin/activate
(venv) pi@raspberrypi:~/honey_dispenser $ pip3 install -r requirements.txt
(venv) pi@raspberrypi:~/honey_dispenser $ deactivate
```

### Run

```console
pi@raspberrypi:~ $ honey_dispenser/venv/bin/dispenser
```


### Cooling Service

1. Create a Systemd Service

Copy service/fan_controller.service to /etc/systemd/system/fan_controller.service:
    
    sudo cp service/fan_controller.service /etc/systemd/system/fan_controller.service


2. Enable the Service

Run the following commands:

    sudo chmod +x /home/pi/fan_controller.py  # Ensure it's executable
    sudo systemctl daemon-reload  # Reload systemd
    sudo systemctl enable fan_controller.service  # Enable service on boot
    sudo systemctl start fan_controller.service  # Start the service now


3. Check if the service is running:

    sudo systemctl status fan_controller.service

Or to view live logs:

    journalctl -u fan_controller.service -f