Add-Type -TypeDefinition @'
using System.Runtime.InteropServices;
[Guid("D666063F-1587-4E43-81F1-B948E807363F"), InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
interface IMMDevice {
    int a(); int o();
    int GetId([MarshalAs(UnmanagedType.LPWStr)] out string id);
}
[Guid("A95664D2-9614-4F35-A746-DE8DB63617E6"), InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
interface IMMDeviceEnumerator {
    int f();
    int GetDefaultAudioEndpoint(int dataFlow, int role, out IMMDevice endpoint);
}
[ComImport, Guid("BCDE0395-E52F-467C-8E3D-C4579291692E")] class MMDeviceEnumeratorComObject { }
public class Audio {
    public static string GetDefault (int direction) {
    var enumerator = new MMDeviceEnumeratorComObject() as IMMDeviceEnumerator;
    IMMDevice dev = null;
    Marshal.ThrowExceptionForHR(enumerator.GetDefaultAudioEndpoint(direction, 1, out dev));
    string id = null;
    Marshal.ThrowExceptionForHR(dev.GetId(out id));
    return id;
    }
}
'@
function getDefaultDevice() {
    $id = [audio]::GetDefault(0)
    Write-Host $id
}
function getFriendlyName($id) {
    $reg = "HKLM:\SYSTEM\CurrentControlSet\Enum\SWD\MMDEVAPI\$id"
    return (get-ItemProperty $reg).FriendlyName
}
function getSimpleName($fullname){
    $nope = $fullname -match "(.*)( \()"
    return $Matches[1]
}
function enableDevice($id) {
    $default_device_fullname = $(getFriendlyName $id)
    $default_device_name = $(getSimpleName($default_device_fullname))
    nircmd.exe setdefaultsounddevice $default_device_name
}
