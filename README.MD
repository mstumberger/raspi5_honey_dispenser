# Set rpi to performance

    echo performance | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor
performance


## Build and Install

[lgpio](http://abyz.me.uk/lg/index.html) is required to be installed. It may be available to you via apt:

```console
sudo apt-get install -y liblgpio-dev
```

If it is not available, manually build and install it by following the instructions [here](https://abyz.me.uk/lg/download.html#Download&Install).

```console
pi@raspberrypi:~ $ git clone --depth=1 https://github.com/endail/hx711
pi@raspberrypi:~ $ cd hx711
```

For RPi 5 the expansion header GPIO pins are now on /dev/gpiochip4 instead of /dev/gpiochip0.

I got the hx711 library to work by changing Utility::openGpioHandle(0) to Utility::openGpioHandle(4), respectively in HX711.cpp.

```console
pi@raspberrypi:~/hx711 $ make && sudo make install
```

## install python dependencies
```console
pi@raspberrypi:~/ $ pip3 install -r requirements.txt
```

## Run


```console
pi@raspberrypi:~/raspi5_honey_dispenser $ cd src
pi@raspberrypi:~/raspi5_honey_dispenser/src $ python .
```

