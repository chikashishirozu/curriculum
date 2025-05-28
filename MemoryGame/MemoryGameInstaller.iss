[Setup]
AppName=MemoryGame
AppVersion=1.0
DefaultDirName={pf}\MemoryGame
DefaultGroupName=MemoryGame
OutputDir=output
OutputBaseFilename=MemoryGameSetup
Compression=lzma
SolidCompression=yes
PrivilegesRequired=admin

[Files]
Source: "dist\MemoryGame005.exe"; DestDir: "{app}"
Source: "cards\*.*"; DestDir: "{app}\cards"; Flags: recursesubdirs createallsubdirs
Source: "fonts\*.*"; DestDir: "{app}\fonts"; Flags: recursesubdirs createallsubdirs

[Icons]
Name: "{group}\MemoryGame"; Filename: "{app}\MemoryGame005.exe"
Name: "{commondesktop}\MemoryGame"; Filename: "{app}\MemoryGame005.exe"; Tasks: desktopicon

[Languages]
Name: "en"; MessagesFile: "compiler:Default.isl"
Name: "ja"; MessagesFile: "compiler:Languages\Japanese.isl"

[Tasks]
Name: "desktopicon"; Description: "デスクトップアイコンを作成"; GroupDescription: "追加アイコン"
