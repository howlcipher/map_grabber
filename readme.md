# Map Grabber

## Overview
Map Grabber is a simple tool designed to facilitate the downloading and installation of maps for Left 4 Dead 2 from a specified website. It provides a graphical user interface (GUI) for browsing available maps and downloading them directly to the user's specified directory.

## Features
- Browse available maps from a specified website.
- Download maps directly from the GUI interface.
- Choose a custom directory for downloading maps.
- Progress bar to track download progress.
- Automatically unzip downloaded files and move them to the specified directory.

## Prerequisites
- **Python 3.x** installed on your system.
- **Ruby** installed on your system.

## Installation
1. Clone or download this repository to your local machine.
2. Make sure you have Python 3.x and Ruby installed on your system.

## Usage
1. Open a terminal or command prompt.
2. Navigate to the directory where the scripts are located.
3. Run the Python script by executing `python map_grabber.py` command.
4. Follow the instructions on the GUI interface to browse and download maps.
5. Similarly, run the Ruby script by executing `ruby map_grabber.rb` command.

## Customization
- You can customize the default download directory by editing the `default_download_directory` variable in the script files.
- Modify the `website_url` variable to point to the website where the maps are hosted.

## Distrubutable
- Built using Python version of the script
- Requires Pyinstaller to build

## How to build the python script
- Run in cmd from the directory of the script.
  
```pyinstaller --hidden-import=tkinter --hidden-import=tkinter.ttk --hidden-import=tkinter.messagebox --hidden-import=tkinter.filedialog --hidden-import=urllib --hidden-import=os --hidden-import=zipfile --hidden-import=bs4 --noconsole --onefile .\map_grabber.py```