; �ű��� Inno Setup �ű��� ���ɣ�
; �йش��� Inno Setup �ű��ļ�����ϸ��������İ����ĵ���

[Setup]
; ע��: AppId ֵ����Ψһʶ���Ӧ�ó���
; ��ֹ������Ӧ�ó���İ�װ��ʹ����ͬ�� AppId ֵ��
; (��Ҫ����һ���µ� GUID����ѡ�񡰹��� | ���� GUID����)
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
; ע��: ��Ҫ���κι���ϵͳ�ļ���ʹ�á�Flags: ignoreversion��?

[Icons]
Name: "{group}\PtServer"; Filename: "{app}\App.exe"
Name: "{group}\{cm:ProgramOnTheWeb,PtServer}"; Filename: "http://www.ptphp.com/"
Name: "{group}\{cm:UninstallProgram,PtServer}"; Filename: "{uninstallexe}"
Name: "{commondesktop}\PtServer"; Filename: "{app}\App.exe"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\PtServer"; Filename: "{app}\App.exe"; Tasks: quicklaunchicon

[Run]
Filename: "{app}\App.exe"; Description: "{cm:LaunchProgram,PtServer}"; Flags: nowait postinstall skipifsilent