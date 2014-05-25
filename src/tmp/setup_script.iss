; 脚本由 Inno Setup 脚本向导 生成！
; 有关创建 Inno Setup 脚本文件的详细资料请查阅帮助文档！

[Setup]
; 注意: AppId 值用于唯一识别该应用程序。
; 禁止对其他应用程序的安装器使用相同的 AppId 值！
; (若要生成一个新的 GUID，请选择“工具 | 生成 GUID”。)
AppId={{88B330D8-B45E-4CFE-A0FC-DA690A4570B5}
AppName=PtServer
AppVerName=PtServer V1.0
AppPublisher=PtPHP
AppPublisherURL=http://www.ptphp.com/
AppSupportURL=http://www.ptphp.com/
AppUpdatesURL=http://www.ptphp.com/
DefaultDirName=D:\PtServer
UsePreviousAppDir=yes
DefaultGroupName=PtServer
AllowNoIcons=yes
OutputBaseFilename=setup
Compression=lzma
SolidCompression=yes

[Languages]
Name: "chinese"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "E:\workspace\PtServer\dist\App.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "E:\workspace\PtServer\dist\config.cfg"; DestDir: "{app}"; Flags: ignoreversion
Source: "E:\workspace\PtServer\dist\w9xpopen.exe"; DestDir: "{app}"; Flags: ignoreversion

Source: "E:\workspace\PtServer\dist\imageformats\*"; DestDir: "{app}\imageformats"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "E:\workspace\PtServer\dist\Microsoft.VC90.CRT\*"; DestDir: "{app}\Microsoft.VC90.CRT"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "E:\workspace\PtServer\dist\var\*"; DestDir: "{app}\var"; Flags: ignoreversion recursesubdirs createallsubdirs
; 注意: 不要在任何共享系统文件上使用“Flags: ignoreversion”?

[Icons]
Name: "{group}\PtServer"; Filename: "{app}\App.exe"
Name: "{group}\{cm:ProgramOnTheWeb,PtServer}"; Filename: "http://www.ptphp.com/"
Name: "{group}\{cm:UninstallProgram,PtServer}"; Filename: "{uninstallexe}"
Name: "{commondesktop}\PtServer"; Filename: "{app}\App.exe"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\PtServer"; Filename: "{app}\App.exe"; Tasks: quicklaunchicon

[Run]
Filename: "{app}\App.exe"; Description: "{cm:LaunchProgram,PtServer}"; Flags: nowait postinstall skipifsilent