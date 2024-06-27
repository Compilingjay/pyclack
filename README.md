# PyClack
A simple, cross-platform* [^1] autoclicker where you can set hotkeys to start or stop the autoclicker, and can the clicks per second done by the autoclicker.

## Running
Download the files and ensure you have the required dependencies, then run:

```
python main.py
```

If you want more direct control of the settings, you can edit the values inside the autosave.ini file if it is present. You edit the default.ini file if you are launching the app for the first time and the autosave does not exist yet.

## Dependencies
PyClack is tested for Python 3.12.2 and uses the following libraries:
```
- PySide6 6.7.1
- keyboard 0.13.5
- mouse 0.7.1
```
PySide6 is a port of Qt for Python (c) 2024 The Qt Project, distributed under the LGPLv3 license.
You can find instructions for installing PySide6 via pip here: https://pypi.org/project/PySide6/
And a link to the repository for PySide6 here: https://code.qt.io/cgit/pyside/pyside-setup.git/

The keyboard and mouse libraries are (c) 2016 BoppreH, distributed under the MIT License.
You can find the keyboard library here: https://github.com/boppreh/keyboard
And the mouse library here: https://github.com/boppreh/mouse

You can find the licenses under the licenses directory.

[^1]: *The mouse and keyboard libraries support Windows and Linux, but sudo is required in order to run the libraries on Linux. MacOS support is experimental. Refer to the keyboard/mouse libraries on GitHub for more details.