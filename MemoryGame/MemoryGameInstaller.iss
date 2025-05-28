pascal
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
Source: "data\*"; DestDir: "{app}\data"; Flags: recursesubdirs

[Icons]
Name: "{group}\MemoryGame"; Filename: "{app}\MemoryGame005.exe"
Name: "{desktop}\M

[Languages]
Name: "ja"; MessagesFile: "compiler:Default.isl"
Name: "en"; MessagesFile: "compiler:Languages\Japanese.isl"

[Tasks]
Name: "desktopicon"; Description: "デスクトップアイコンを作成"; GroupDescription: "追加アイコン"
