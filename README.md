# Mouse Info

Mouse Info is a real-time tracking tool that provides valuable insights into the mouse cursor's behavior. With features like position tracking, pixel color detection, magnification, and system resource monitoring, it offers a comprehensive view of mouse activity.

![Screenshot of the user interface of Mouse_Info.](/mouse_position.png)

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Settings](#settings)
- [Building Standalone Executable](#building-standalone-executable)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Mouse Location Tracking**: Displays the current X and Y coordinates of the cursor.
- **Pixel Color Detection**: Shows the color of the pixel under the cursor in both DEC and HEX formats.
- **Magnification**: Provides a magnified view of the area around the cursor, with a customizable bullseye at the center.
- **CPU/Memory Monitoring**: Monitors the CPU and memory usage of the program with a 10-second update interval.
- **Customizable Settings**: Allows users to enable or disable various features, including CPU/Memory tracking and magnification.

## Installation

Clone the repository and install the required dependencies:

```
git clone https://github.com/username/mouse-info.git
cd mouse-info
pip install -r requirements.txt
```

## Usage

Run the \`Mouse_Info.py\` file to launch Mouse Info:

```
python Mouse_Info.py
```

### Controls

- **Pause/Resume Button**: Stops and resumes tracking (Shortcut: Ctrl-S).
- **Help Button**: Opens a help window with instructions (Shortcut: F1).
- **Settings Button**: Allows enabling or disabling various features.

## Settings

Access the Settings window to customize Mouse Info with the following options:

- **Enable CPU/Memory Tracking**: Toggles tracking of CPU and memory usage.
- **Enable Magnification**: Toggles the magnified view.
- **Enable Hex Color**: Toggles displaying the pixel color in HEX format.
- **Enable Dec Color**: Toggles displaying the pixel color in DEC format.

## Building Standalone Executable

You can package Mouse Info into a standalone executable using PyInstaller:

```
pip install pyinstaller
pyinstaller --onefile Mouse_Info.py
```

Find the executable in the \`dist\` directory.

## Contributing

Contributions are welcome! Please read the [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute to Mouse Info.

## License

Mouse Info is licensed under the GNU General Public License v3.0. See the [LICENSE.md](LICENSE.md) file for details.
