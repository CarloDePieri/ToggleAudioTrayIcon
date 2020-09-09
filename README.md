# ToggleAudioTrayIcon

This is a Windows tray icon widget that can toggle between two audio devices and will show an 
icon representing the active one.

## Dependencies

The tool depends on [nircmd](https://www.nirsoft.net/utils/nircmd.html) for the actual device toggling, so it must be included in the `$PATH`.

## Latest Release

#### Usage

The quickest way to get the tool is to download the [latest release](https://github.com/CarloDePieri/ToggleAudioTrayIcon/releases/latest).

Extract the zipped folder where you want to keep the tool. 

Run it by double clicking on `ToggleAudioTrayIcon.exe`.

#### Customize icons and devices names

In the `config.ini` file you can modify fields to customize icons' and devices' names.

## Build from source

#### Prerequisites

You will need `Python 3.7` and `pipenv` installed.

#### Download

With git:

```
$ git clone https://github.com/CarloDePieri/ToggleAudioTrayIcon.git 
```

#### Install

To install all script dependencies launch:

```
$ install.bat
```

#### Run directly from python

To launch the app, create a link that points to the venv `pythonw`, with the script file as argument:

```
path_to_venv\Script\pythonw.exe toggle_app.py
```

Remember to set the current directory as the one containing `toggle_app.py`.

#### Build executable

Launch

```
$ build.bat
```

This will generate a `dist` folder which will contain a folder called `ToggleAudioTrayIcon`. Move this folder
wherever you wish to keep this utility.

You can now delete all source folders, including the venv.
