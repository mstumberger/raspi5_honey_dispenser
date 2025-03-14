#!/bin/bash

# Prompt for the name of the application
app_name="HoneyDispenser"

# Get the directory of the current script (shortcut folder)
shortcut_dir="$(dirname "$(realpath "$0")")"

# Get the project root by using dirname on the shortcut directory
project_root="$(dirname "$shortcut_dir")"

# Set the script path dynamically based on the project root
#script_path="venv/bin/python3 $project_root/src/mstumb"
script_path="venv/bin/dispenser"


# Path to the icon file
icon_path="$shortcut_dir/icon.png"

# Display the script and icon paths for verification
echo "Using script path: $script_path"
echo "Using icon path: $icon_path"

# Get the current user's home directory dynamically
user_home="$HOME"

# Set the desktop entry file path dynamically based on the current user's Desktop directory
desktop_file="$app_name.desktop"
desktop_file_path="$user_home/Desktop/$desktop_file"

# Create the .desktop file
echo "Creating desktop shortcut at $desktop_file_path..."

cat <<EOL > "$desktop_file_path"
[Desktop Entry]
Version=1.0
Name=$app_name
Comment=Launch $app_name Application
Path=$project_root
Exec=$project_root/$script_path
Icon=$icon_path
Terminal=false
Type=Application
Categories=Application
EOL

# Make the .desktop file executable
chmod +x $desktop_file_path

# Add to applications menu
sudo cp $desktop_file_path /usr/share/applications/
# Make the .desktop file executable
sudo chmod +x /usr/share/applications/$desktop_file
# Refresh the menu
lxpanelctl restart

echo "Desktop shortcut created successfully at $desktop_file_path and /usr/share/applications/$desktop_file!"
