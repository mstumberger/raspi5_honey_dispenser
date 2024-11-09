# Set rpi to performance

    echo performance | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor


## Build and Install c++ dependencies

[lgpio](http://abyz.me.uk/lg/index.html) is required to be installed. It may be available to you via apt:

```console
sudo apt-get install -y liblgpio-dev
```

If it is not available, manually build and install it by following the instructions [here](https://abyz.me.uk/lg/download.html#Download&Install).

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

## install python dependencies

```console
pi@raspberrypi:~/ $ pip3 install -r requirements.txt
```

## Run

```console
pi@raspberrypi:~/raspi5_honey_dispenser $ cd src
pi@raspberrypi:~/raspi5_honey_dispenser/src $ python .
```

