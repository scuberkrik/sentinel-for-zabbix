!include LogicLib.nsh

RequestExecutionLevel admin

Name "install SentinelForZabbix"
OutFile "Sentinel for zabbix.exe"
InstallDir "$PROGRAMFILES\SentinelForZabbix"

Page InstFiles

Var AllowChangeDir

Function .onInit
    StrCpy $AllowChangeDir 1
FunctionEnd

Function LeaveDirectory
    StrCpy $AllowChangeDir 0
FunctionEnd

Section
    InitPluginsDir
    CreateDirectory "$INSTDIR"
    nsExec::Exec '"python-3.12.3-amd64.exe" /quiet InstallAllUsers=1 PrependPath=1'
    nsExec::Exec '"C:\Program Files\Python312\Scripts\pip.exe" install requests'
	nsExec::Exec '"C:\Program Files\Python312\Scripts\pip.exe" install schedule'
    SetOutPath "$INSTDIR"
    File "zabbix_agentd.conf"
    File "pars_xml.py"
    File "conf_agent.py"
    File "start_agent.ps1"
	File "service.ps1"
	File "service.py"
    nsExec::Exec '"C:\Program Files\Python312\python.exe" "$INSTDIR\pars_xml.py"'
    nsExec::Exec '"C:\Program Files\Python312\python.exe" "$INSTDIR\conf_agent.py"'
    nsExec::Exec 'powershell.exe -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File "$INSTDIR\start_agent.ps1"'
    nsExec::Exec 'powershell.exe -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File "$INSTDIR\service.ps1"'

    Delete "$INSTDIR\zabbix_agentd.conf"
    Delete "$INSTDIR\conf_agent.py"
    Delete "$INSTDIR\start_agent.ps1"
    Delete "$INSTDIR\pars_xml.py"
	Delete "$INSTDIR\service.py"
	Delete "$INSTDIR\service.ps1"
SectionEnd

Function .onSelChange
    ${If} $AllowChangeDir == 0
        Abort
    ${EndIf}
FunctionEnd

Section "Uninstall"
    ; Удаление директории
    RMDir "$INSTDIR"
SectionEnd