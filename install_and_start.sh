#!/bin/bash

# Save the current directory (start location)
START_LOCATION=$(pwd)

#set rpi to performance mode
echo performance | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor

# Install the necessary dependencies
sudo apt-get install -y liblgpio-dev

# Clone the repository
cd ~
git clone --depth=1 https://github.com/endail/hx711
cd hx711

# Check for Raspberry Pi 5 by checking the device model
if grep -q "Raspberry Pi 5" /proc/device-tree/model; then
    echo "Running on Raspberry Pi 5, applying patch"
    cd src
    sed -i 's/Utility::openGpioHandle(0)/Utility::openGpioHandle(4)/g' HX711.cpp
    cd ..
else
    echo "Not running on Raspberry Pi 5"
fi

# Build and install the library
make && sudo make install

# Navigate back to the original location and set up the Python environment
cd $START_LOCATION

python3 -m venv venv

# Use a subshell to run the environment
(
    source venv/bin/activate
    pip3 install -r requirements.txt

    # Call the script to create the desktop shortcut
    echo "Creating desktop shortcut..."
    bash shortcut/create_desktop_shortcut.sh

    # Run the Python script
    cd src
    python3 .
)