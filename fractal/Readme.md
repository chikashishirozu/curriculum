# Some font settings need to be modified and dependencies need to be installed. A virtual environment needs to be created.

$ sudo apt update

$ sudo apt install python3-dev python3-pyqt5 python3-matplotlib

$ sudo apt install -y make build-essential libssl-dev zlib1g-dev \
    libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
    libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev \
    liblzma-dev

$ git clone https://github.com/pyenv/pyenv.git ~/.pyenv   

$ echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc

$ echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc

$ echo 'eval "$(pyenv init --path)"' >> ~/.bashrc
 
$ source ~/.bashrc

$ pyenv install anaconda3-2024.10-1

$ conda create -n mayavi_env -c conda-forge python=3.11 mayavi traits pyface vtk numba

$ conda activate mayavi_env
