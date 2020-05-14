# ToggleAudioWidget

This is a Windows tray icon widget that can toggle between two audio devices and will show an 
icon to show the active one.


#### Prerequisites

You will need `Python 3.8` and `pipenv` installed.

#### Install

To install all script dependencies launch:

```
$ python -m venv .venv
$ pipenv install
```

#### Run

To launch the app, create a link that points to the venv `pythonw`, with the script file as argument:

```
path_to_venv\Script\pythonw.exe toggle_app.py
```

Remember to set the current directory as the one containing `toggle_app.py`.


#### Customize icons and devices names

In the `toggle_app.py` file you can modify fields inside `AudioController` to customize icons and devices.
