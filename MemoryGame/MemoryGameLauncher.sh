#!/bin/bash
# 仮想環境を有効化し、アプリを起動する

cd /home/hiroppy123/MemoryGame || exit

# 例：venv の場合
source venv/bin/activate

# 例：conda の場合（conda 初期化済み前提）
# source ~/anaconda3/etc/profile.d/conda.sh
# conda activate memorygame_env

# アプリ起動
python3 MemoryGame0055.py

