$render = "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\MMDevices\Audio\Render"
$title_key = "{a45c254e-df1c-4efd-8020-67d146a850e0},2"
$id = 0

Get-ChildItem -Path $render | ForEach-Object  {
  if ($id++ -eq 0) {
    $name = "Philips 244E"
  }
  else {
    $name = "G35"
  }
  Set-ItemProperty -Force -Path Registry::$_\Properties -Name $title_key -Value $name
}
