[Tasks]
Name: desktopicon; Description: Create a desktop icon; Flags: unchecked
Name: associate; Description: Associate with Dehacked patch files


[Files]
Source: .\build\exe.win-amd64-3.10\*.*; DestDir: {app}; Flags: recursesubdirs createallsubdirs
Source: .\fonts\dejavu-sans-mono\DejaVuSansMono.ttf; DestDir: {autofonts}; Flags: onlyifdoesntexist uninsneveruninstall; FontInstall: DejaVu Sans Mono
Source: .\fonts\dejavu-sans-mono\DejaVuSansMono-Bold.ttf; DestDir: {autofonts}; Flags: onlyifdoesntexist uninsneveruninstall; FontInstall: DejaVu Sans Mono Bold


[Icons]
Name: {group}\whacked64; Filename: {app}\whacked64.exe; WorkingDir: {app}; IconFilename: {app}\res\icon-hatchet.ico; IconIndex: 0
Name: {userdesktop}\whacked64; Filename: {app}\whacked64.exe; WorkingDir: {app}; IconFilename: {app}\res\icon-hatchet.ico; IconIndex: 0; Tasks: " desktopicon"
Name: {group}\{cm:UninstallProgram, whacked64}; Filename: {uninstallexe}


[Setup]
InternalCompressLevel=ultra64
SolidCompression=true
AppName=WhackEd64
AppVerName=whacked64 1..0.0
DefaultDirName={autopf}\WhackEd64
AlwaysUsePersonalGroup=false
ShowLanguageDialog=no
AppVersion=1.0.0
UninstallDisplayIcon={app}\whacked64.exe
UninstallDisplayName=WhackEd64
AppendDefaultGroupName=true
DefaultGroupName=WhackEd64
Compression=lzma2/ultra64
OutputDir=.
SourceDir=.
OutputBaseFilename=whacked64-setup-1.0.0
AllowNoIcons=true
PrivilegesRequired=admin
ChangesAssociations=true
InfoBeforeFile=
LicenseFile=LICENSE
FlatComponentsList=true
UninstallLogMode=overwrite
LanguageDetectionMethod=none
WizardImageStretch=false
RestartIfNeededByRun=false
AppID={{A8A56AC6-E82B-49AD-9093-5AC204830F89}


[Run]
Filename: {app}\whacked64.exe; WorkingDir: {app}; Description: Run WhackEd64; Flags: nowait postinstall hidewizard skipifsilent


[InstallDelete]
Name: {app}\cfg\tables_mbf_beta.json; Type: files


[UninstallDelete]
Name: {app}\res; Type: filesandordirs
Name: {app}\cfg; Type: filesandordirs
Name: {app}\*.*; Type: files
Name: {app}; Type: dirifempty
Name: {userappdata}\whacked64; Type: filesandordirs


[Registry]
Root: HKCR; SubKey: "WhackEd64"; ValueType: String; ValueName: ""; ValueData: "WhackEd64 patch file"; Flags: uninsdeletekey; Tasks: associate
Root: HKCR; Subkey: "WhackEd64\DefaultIcon"; ValueType: String; ValueName: ""; ValueData: "{app}\res\icon-document.ico,0"; Flags: uninsdeletekey; Tasks: associate

Root: HKCR; SubKey: "WhackEd64\Shell\Open\Command"; ValueType: String; ValueName: ""; ValueData: """{app}\whacked64.exe"" -workdir ""{app}"" -open ""%1"""; Flags: uninsdeletekey; Tasks: associate

Root: HKCR; SubKey: ".deh"; ValueType: String; ValueName: ""; ValueData: "WhackEd64"; Flags: uninsdeletekey; Tasks: associate
Root: HKCR; SubKey: ".bex"; ValueType: String; ValueName: ""; ValueData: "WhackEd64"; Flags: uninsdeletekey; Tasks: associate
