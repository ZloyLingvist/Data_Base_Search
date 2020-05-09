SET /P _inputname= Your Python 3 (x64) version is above 3.8:Y/N
IF "%_inputname%"=="Y" GOTO :install_block
echo You need Python 3 above 3.8 (x64)
GOTO :end
:install_block
echo Install TatSu
pip install tatsu
echo Install torch
pip install torch==1.4.0+cpu torchvision==0.5.0+cpu -f https://download.pytorch.org/whl/torch_stable.html
echo Install stanza
pip install stanza
echo Install numpy
pip install numpy
echo Install pyyaml
pip install pyyaml
echo Install pymorphy2
pip install pymorphy2
echo Install pydotplus
pip install pydotplus
echo Download (check on exist) stanza models (need Internet connection)
Script\install.py
pause
:end