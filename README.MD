# Raspberry PI 5 honey dispenser

# Material

| Part                                      | Price  | URL                                                                                              |
|-------------------------------------------|--------|--------------------------------------------------------------------------------------------------|
| 3D printed parts                          | ~5€    | https://github.com/mstumberger/raspi5_honey_dispenser/tree/master/stl                            |
| Raspberry pi 5                            | 76.19€ | https://si.farnell.com/raspberry-pi/rpi5-8gb-single/raspberry-pi-5-model-b-8gb-2-4ghz/dp/4256000 |
| MicroSD card 32GB                         | 12.90€ | https://si.farnell.com/multicomp-pro/ts32gusd420t-mcp/mircosd-card-32gb-raspberry-pi/dp/3879376  |
| Power supply                              | 12.48€ | https://si.farnell.com/raspberry-pi/sc1157/power-supply-usb-c-5-1v-5a-black/dp/4263045           |
| USB Extension cable 0.3m                  | 6.5€   | https://www.aliexpress.com/item/1005003488021890.html                                            |
| 5" touch screen                           | 27.94€ | https://www.aliexpress.com/item/1005007314274603.html                                            |
| 90° HDMI cable (conn. A2, D2, cable 30cm) | 9.09€  | https://www.aliexpress.com/item/1005005945873056.html                                            |
| 90° USB cable (AMUP-V8UP, 30CM)           | 6.57€  | https://www.aliexpress.com/item/1005005978243043.html                                            |
| 5kg Load Cell with HX711 Amplifier        | 5.75€  | https://www.aliexpress.com/item/1005005990685261.html                                            |
| 10x 2.54MM Pitch 30CM Dupont Line Wire    | 3.19€  | https://www.aliexpress.com/item/1005005924705004.html                                            |
| Connectors for motor connection           | 5.21€  | https://www.aliexpress.com/item/1005004891694780.html                                            |
| Connection wire 22AWG (1/3)               | 6.08€  | https://www.aliexpress.com/item/1005006516374385.html                                            |
| MG996R Servo motor                        | 5.35€  | https://www.aliexpress.com/item/1005007552788835.html                                            |
| Piezzo buzzer                             | 0.23€  | https://www.aliexpress.com/item/1005006260328559.html                                            |
| PWM Cooling Fan                           | 7.86€  | https://www.aliexpress.com/item/1005004219041650.html                                            |
| RGB LED                                   | 0.04€  | https://www.aliexpress.com/item/1005005990835193.html                                            |
| SMD R150 and 2x R33                       | 0.01€  | https://www.aliexpress.com/item/1005006823361841.html                                            |
| PCB Proto-board                           | 0.30€  | https://www.aliexpress.com/item/1005006665029598.html                                            | 
| 8x M2.5 Brass Hot Melt Nut Insert + bolt  | ~0.18€ | https://www.aliexpress.com/item/1005006760493119.html                                            |

Total costs:

    ~190.87€


# Wiring

-	HX711 - GND 39, VCC 17, DT 40, SCK 38 (Weight)
-	Servo - GND 6, VCC 2, Signal 12 (Dosing)
-	Fan - GND 9, VCC 4 (PWM fan)	
-   Piezzo - Signal 36 (Audio Signal)
-	RGB LED - GND 14, Green 16, Blue 15, Red 13

![schematics](img/wiring%20schematics.jpg)


# Assembly instructions

1. Print STL Files for all components.
2. Insert Brass Insert Nuts into mounting locations on Raspberry Pi 5, signalization proto-board, HX711 amplifier, and display holder.
3. Solder Components: Attach the Piezo and RGB LED to the proto-board, create a common ground, and use connectors for wiring to the Raspberry Pi.
4. Mount Touchscreen: Connect the USB and HDMI cables to the touchscreen, then mount it onto the "stl/Scale - Display holder v5.stl" using 4 M2.5 screws.
5. Prepare Servo Motor Wiring: Solder 3 wires to a male connector for controlling the servo motor, then place the connector into the display holder.
6. Install USB-C Extension: Mount the USB-C extension onto the display holder using provided screws.
7. Mount Load Cell: Attach the load cell to the display holder at the designated mounting point, ensuring the correct orientation. Also attach Scaling surface to the other end of the load cell.
8. Wire Connection: Route and connect the cables inside the housing to the HX711 amplifier, securing them with M2.5 screws.
9. Prepare MicroSD Card: Load Raspbian OS onto the microSD card and insert it into the Raspberry Pi card slot.
10. Install Raspberry Pi: Place the Raspberry Pi into its dedicated space in the holder and secure it with M2.5 screws. Connect the microHDMI and USB-C cables.
11. Connect Display Cables: Route the USB cable for the touch display through the designated space in the cover, then place the cover on the scale base, ensuring it clicks into place.
12. Power On: Connect the USB and power adapter to the scale, plug the power adapter into a socket, and wait for the Raspberry Pi to boot.
13. Prepare Servo Motor Cable: Solder two female connectors to the servo motor control cable.
14. Connect to Lid Adapter: Cut the servo motor wires, solder them to the male connector fixed in the "stl/Lid adapter - top.stl."
15. Attach Lid Adapter: Use two nuts and bolts to secure the lid adapter to the honey dispenser.
16. Install Servo Motor Handles: Attach the large handle to the servo motor adapter and secure it vertically. Fix the small handle by drilling a hole and using a screw.
17. Disconnect Large Handle for initial installation.
18. Motor Calibration: Once the application starts and the motor moves to position 0, reattach the large handle.
19. Calibrate Scale: Calibrate the scale using a known weight to ensure accuracy.
20. Start Honey Dispensing: Once calibration is complete and saved, you can begin dispensing honey

![schematics](img/honey_dispenser.gif)

## Install
This script will automatically:
- apply patch for Raspberry PI 5 HX711 library,
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
(venv) pi@raspberrypi:~/honey_dispenser $ pip3 install .
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

### Tkiter application service

1. Create a Systemd Service

Copy service/tkinter_app.service to /etc/systemd/system/tkinter_app.service:

    
    sudo cp service/tkinter_app.service /etc/systemd/system/tkinter_app.service


2. Enable the Service

Run the following commands:

    sudo systemctl daemon-reload  # Reload systemd
    sudo systemctl enable tkinter_app.service  # Enable service on boot
    sudo systemctl start tkinter_app.service  # Start the service now


3. Check if the service is running:


    sudo systemctl status tkinter_app.service

Or to view live logs:

    journalctl -u tkinter_app.service -f


4. Stop running service:


    sudo systemctl stop tkinter_app.service


# Shutdown

To allow passwordless shutdown, you can edit the sudoers file:


    sudo visudo


Add the following line :

    pi ALL=(ALL) NOPASSWD: /sbin/shutdown