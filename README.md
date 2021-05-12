# pomerium-gui
A Simple Gui For Pomerium Beyond Corp TCP Access

Yo must first install and configure Pomerium properly:  https://github.com/pomerium/pomerium


Requires Python 3.6 or greater

  1. Update the SERVER variable to point it at your pomerium server. 
  2. pip3 install -r requirements.txt
  3. python pomerium-gui.py 

For windows you may create an exe file by running: 
  pip3 install pyinstaller
  pyinstaller -wF pomerium.py
