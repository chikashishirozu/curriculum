# Some font settings need to be modified and dependencies need to be installed. A virtual environment needs to be created.

$ sudo apt install python3-dev python3-pyqt5 python3-matplotlib

$ conda create -n mayavi_env -c conda-forge python=3.11 mayavi traits pyface vtk numba

$ conda activate mayavi_env
