import re
import subprocess
from types import ModuleType

import reusables
import wx
from wx.adv import TaskBarIcon
import logging
import argparse


class AudioController:
    def __init__(self):
        # Recover configs
        config = reusables.config_dict("config.ini")
        self.name_device_a = config["device_a"]["name"]
        self.name_device_b = config["device_b"]["name"]
        self.icon_device_a = config["device_a"]["icon"]
        self.icon_device_b = config["device_b"]["icon"]

    @staticmethod
    def _force_portaudio_reload(sounddevice: ModuleType) -> None:
        """Cause the PortAudio library inside the given sounddevice module to be reloaded.

        Without doing this the default device is not refreshed after changing it."""
        sounddevice._ffi.dlclose(sounddevice._lib)
        sounddevice._lib = sounddevice._ffi.dlopen(sounddevice._libname)
        sounddevice._lib.Pa_Initialize()

    def get_default_device_name(self) -> str:
        import sounddevice

        # force sounddevice to reload the default device from the PortAudio dll
        # noinspection PyTypeChecker
        self._force_portaudio_reload(sounddevice)
        # now get the raw name of the device
        idd = sounddevice.default.device[1]
        raw_name = sounddevice.query_devices(idd)["name"]
        # extract the name and return it
        matches = re.finditer(r".*(?= \()", raw_name, re.MULTILINE)
        return next(matches).group()

    def set_default_device(self, device_name: str) -> None:
        subprocess.run(
            ["nircmd.exe", "setdefaultsounddevice", "{}".format(device_name)]
        )

    def toggle_between_devices(self) -> None:
        default_device_name = self.get_default_device_name()
        if default_device_name == self.name_device_a:
            self.set_default_device(self.name_device_b)
        else:
            self.set_default_device(self.name_device_a)

    def open_sound_panel(self, event):
        subprocess.run(["control", "mmsys.cpl", "sounds"])


def create_menu_item(menu, label, func):
    item = wx.MenuItem(menu, -1, label)
    menu.Bind(wx.EVT_MENU, func, id=item.GetId())
    menu.Append(item)
    return item


class MyTaskBarIcon(TaskBarIcon):
    def __init__(self, frame):
        self.AC = AudioController()
        self.frame = frame
        super(TaskBarIcon, self).__init__()
        self.set_icon()
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.on_left_down)

    def CreatePopupMenu(self):
        menu = wx.Menu()
        create_menu_item(menu, "Open Sound Panel", self.AC.open_sound_panel)
        menu.AppendSeparator()
        create_menu_item(menu, "Exit", self.on_exit)
        return menu

    def set_icon(self):
        default_device_name = self.AC.get_default_device_name()
        logging.debug(f"Current default device name: {default_device_name}")
        if default_device_name == self.AC.name_device_a:
            path = self.AC.icon_device_a
            tooltip = self.AC.name_device_a
        else:
            path = self.AC.icon_device_b
            tooltip = self.AC.name_device_b
        logging.debug(f"Setting icon to: {path}")
        icon = wx.Icon(wx.Bitmap(path))
        self.SetIcon(icon, tooltip)
        logging.debug(f"Icon set")

    def on_left_down(self, event):
        self.AC.toggle_between_devices()
        # Wait a bit to make sure nircmd finish toggling the sound device before updating the icon
        wx.CallLater(int(500), self.set_icon)

    def on_exit(self, event):
        wx.CallAfter(self.Destroy)
        self.frame.Close()


class App(wx.App):
    def OnInit(self):
        frame = wx.Frame(None)
        self.SetTopWindow(frame)
        MyTaskBarIcon(frame)
        return True


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
                        prog = 'ToggleAudioTrayIcon',
                        description = 'A tray icon to quickly toggle default audio device.')
    parser.add_argument('-d', '--debug', action='store_true', help="print debug message to a log file")
    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(
            filename="ToggleAudioTrayIcon_debug_logs.txt",
            filemode="a",
            format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
            datefmt="%H:%M:%S",
            level=logging.DEBUG,
        )
        logging.debug("START")

    app = App(False)
    app.MainLoop()
