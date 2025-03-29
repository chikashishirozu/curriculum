import sys
from cx_Freeze import setup, Executable

# build_exeオプション
build_exe_options = {
    "packages": ["os"],  # 必要なモジュールを指定
    "packages": ["sympy"],
    "excludes": [],
    "include_files": []
}

# baseの設定を削除（Linuxでは不要）
base = None

setup(
    name="calculator",
    version="1.0.0",
    description="Safe Calculator with Sympy",
    options={
        "build_exe": build_exe_options
    },
    executables=[
        Executable(
            "calculator.py",  # メインとなるPythonファイル
        )
    ],
)

