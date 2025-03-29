# build and setup
hiroppy123@fedora:~/音楽/calculator/Linux$ python3 -m venv venv
(venv) hiroppy123@fedora:~/音楽/calculator/Linux$ source venv/bin/activate
(venv) hiroppy123@fedora:~/音楽/calculator/Linux$ pip install cx_Freeze
(venv) hiroppy123@fedora:~/音楽/calculator/Linux$ pip install sympify
(venv) hiroppy123@fedora:~/音楽/calculator/Linux$ python setup.py build
(venv) hiroppy123@fedora:~/音楽/calculator/Linux$ ./build/exe.linux-x86_64-3.13/calculator
