import subprocess
import wx
from wx.adv import TaskBarIcon


class ToggleLibWrapper:

    powershell_bin = "C:\\WINDOWS\\system32\\WindowsPowerShell\\v1.0\\powershell.exe"
    dot_lib = ". \"./toggle-lib\";"

    def get_default_sound_device_id(self) -> str:
        process = subprocess.run([self.powershell_bin, self.dot_lib, "&getDefaultDevice"], capture_output=True)
        return process.stdout.decode("UTF-8").replace("\n", "")

    def enable_device(self, device_id: str) -> None:
        subprocess.run([self.powershell_bin, self.dot_lib, '&enableDevice("{}")'.format(device_id)])

    def toggle_between_devices(self, device_id_a: str, device_id_b: str) -> None:
        default_device = self.get_default_sound_device_id()
        if default_device == device_id_a:
            self.enable_device(device_id_b)
        else:
            self.enable_device(device_id_a)

    def open_sound_panel(self, event):
        subprocess.run(["control", "mmsys.cpl", "sounds"], capture_output=True)


def create_menu_item(menu, label, func):
    item = wx.MenuItem(menu, -1, label)
    menu.Bind(wx.EVT_MENU, func, id=item.GetId())
    menu.Append(item)
    return item


class MyTaskBarIcon(TaskBarIcon):

    id_philips = "{0.0.0.00000000}.{2cf501c7-5a89-419e-abfd-bef3a3b3b27b}"
    id_logitech = "{0.0.0.00000000}.{d1bcb1d0-6f6d-4092-a84b-bab988432708}"

    def __init__(self, frame):
        self.TLW = ToggleLibWrapper()
        self.frame = frame
        super(TaskBarIcon, self).__init__()
        self.set_icon()
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.on_left_down)

    def CreatePopupMenu(self):
        menu = wx.Menu()
        create_menu_item(menu, 'Open Sound Panel', self.TLW.open_sound_panel)
        menu.AppendSeparator()
        create_menu_item(menu, 'Exit', self.on_exit)
        return menu

    def set_icon(self):
        if self.TLW.get_default_sound_device_id() == self.id_philips:
            path = "screen.png"
            tooltip = "Philips 244E"
        else:
            path = "headset.png"
            tooltip = "G35"
        icon = wx.Icon(wx.Bitmap(path))
        self.SetIcon(icon, tooltip)

    def on_left_down(self, event):
        self.TLW.toggle_between_devices(self.id_philips, self.id_logitech)
        self.set_icon()

    def on_exit(self, event):
        wx.CallAfter(self.Destroy)
        self.frame.Close()


class App(wx.App):
    def OnInit(self):
        frame = wx.Frame(None)
        self.SetTopWindow(frame)
        MyTaskBarIcon(frame)
        return True


def main():
    app = App(False)
    app.MainLoop()


if __name__ == '__main__':
    main()
