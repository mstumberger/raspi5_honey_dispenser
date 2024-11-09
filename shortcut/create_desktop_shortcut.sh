#!/bin/bash

# Prompt for the name of the application
app_name="HoneyDispenser"

# Get the directory of the current script (shortcut folder)
shortcut_dir="$(dirname "$(realpath "$0")")"

# Get the project root by using dirname on the shortcut directory
project_root="$(dirname "$shortcut_dir")"

# Set the script path dynamically based on the project root
script_path="$project_root/src"

# Path to the icon file
icon_path="$shortcut_dir/icon.png"

# Display the script and icon paths for verification
echo "Using script path: $script_path"
echo "Using icon path: $icon_path"

# Get the current user's home directory dynamically
user_home="$HOME"

# Set the desktop entry file path dynamically based on the current user's Desktop directory
desktop_file="$user_home/Desktop/$app_name.desktop"

# Create the .desktop file
echo "Creating desktop shortcut at $desktop_file..."

cat <<EOL > "$desktop_file"
[Desktop Entry]
Version=1.0
Name=$app_name
Comment=Launch $app_name Application
Exec=$project_root/venv/bin/python3 $script_path
Icon=$icon_path
Terminal=false
Type=Application
Categories=Application
EOL

# Make the .desktop file executable
chmod +x "$desktop_file"

echo "Desktop shortcut created successfully at $desktop_file!"
