# Some font settings need to be modified and dependencies need to be installed. A virtual environment needs to be created.

# Easy start

$ sudo dnf update

$ sudo dnf install python3-devel python3-tk python3-pillow-tk python3-pillow python3-pillow-dev

$ python3 MemoryGame001.py

# another way

$ sudo apt update && upgrade

$ sudo apt install python3-dev python3-pyqt5 python3-matplotlib

$ sudo apt install -y make build-essential libssl-dev zlib1g-dev
libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm
libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev
liblzma-dev

$ git clone https://github.com/pyenv/pyenv.git ~/.pyenv

$ echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc

$ echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc

$ echo 'eval "$(pyenv init --path)"' >> ~/.bashrc

$ source ~/.bashrc

$ pyenv install anaconda3-2024.10-1

$ conda create -n memorygame_env -c conda-forge python=3.11 mayavi traits pyface vtk numba matplotlib pillow tk

$ conda init

$ source ~/.bashrc

(base)$ conda activate memorygame_env

(memorygame_env)$ python3 MemoryGame001.py

--- (When using MemoryGame.desktop to set up auto-launch with an icon, you must place the MemoryGame.desktop file in .local/share/applicasions and copy the cards and fonts directories to your user directory.) ---

$ python3 -m venv venv

$ source venv/bin/activate

$ pip install pillow tk

$ cp MemoryGame.desktop ~/.local/share/applications
