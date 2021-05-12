import subprocess
import sys
import PySimpleGUI as sg
import socket
import time
import requests
import os.path
from os import path
import zipfile
import tarfile
import platform
from pathlib import Path



SERVER = 'https://someserver.mycompany.com'

sg.theme('Dark Blue 3')

home = str(Path.home())

if 'Windows' in platform.system():
    print('system is windows') 
    PCLI = home + '\\' + 'pomerium-cli.exe'
    print(PCLI)
    print(home)
    #check for pomerium-cli
    if path.exists(PCLI):
        POM = f'powershell.exe -windowstyle hidden -command {PCLI} tcp --pomerium-url {SERVER}'
    else:
        url = 'https://github.com/pomerium/pomerium/releases/download/v0.14.0/pomerium-cli-windows-amd64.zip'
        r = requests.get(url, allow_redirects=True)
        open(f'{home}\pomerium-cli-windows-amd64.zip', 'wb').write(r.content)
        with zipfile.ZipFile(f'{home}\pomerium-cli-windows-amd64.zip', 'r') as zip_ref:
            zip_ref.extractall(f'{home}\\')
            if path.exists(PCLI):
                POM = f'powershell.exe -windowstyle hidden -command {PCLI} tcp --pomerium-url {SERVER}'
            else:
                print('error: unable to install pomerium:')
                sys.exit(1)
elif 'Linux' in platform.system():
    print('System is Linux-checking for Pomerium-cli')
          
    #check for pomerium-cli
    if path.exists(f"{home}/pomerium-cli"):
        POM = f'{home}/pomerium-cli  tcp --pomerium-url {SERVER}'
    else:
        url = 'https://github.com/pomerium/pomerium/releases/download/v0.14.0/pomerium-cli-linux-amd64.tar.gz'
        r = requests.get(url, allow_redirects=True)
        open(f'{home}/pomerium-cli-linux-amd64.tar.gz', 'wb').write(r.content)
        with tarfile.open(f'{home}/pomerium-cli-linux-amd64.tar.gz', 'r:gz') as zip_ref:
            zip_ref.extractall(f'{home}/')
            zip_ref.close()
            if path.exists(f"{home}/pomerium-cli"):
                POM = f'{home}/pomerium-cli  tcp --pomerium-url {SERVER}'
            else:
                print('error: unable to install pomerium:')
                sys.exit(1)
elif 'Darwin' in platform.system():
    print('System is Mac-checking for Pomerium-cli')
          
    #check for pomerium-cli
    if path.exists(f"{home}/pomerium-cli"):
        POM = f'{home}/pomerium-cli  tcp --pomerium-url {SERVER}'
    else:
        url = 'https://github.com/pomerium/pomerium/releases/download/v0.14.0/pomerium-cli-darwin-amd64.tar.gz'
        r = requests.get(url, allow_redirects=True)
        open(f'{home}/pomerium-cli-darwin-amd64.tar.gz', 'wb').write(r.content)
        with tarfile.open(f'{home}/pomerium-cli-darwin-amd64.tar.gz', 'r:gz') as zip_ref:
            zip_ref.extractall(f'{home}/')
            zip_ref.close()
            if path.exists(f"{home}/pomerium-cli"):
                POM = f'{home}/pomerium-cli  tcp --pomerium-url {SERVER}'
            else:
                print('error: unable to install pomerium:')
                sys.exit(1)
    

def main():
    layout = [
        [sg.Output(size=(100,2), font='courier 12', background_color='black', text_color='white')],
        [sg.Multiline(size=(100,10), font='courier 12',  key='-OUTPUT-', do_not_clear=True)],
        [sg.T('IP or Host '), sg.Input(key='-IP-', do_not_clear=False, size=(40, 1)), sg.T('port'), sg.Input(key='-PORT-', do_not_clear=False, size=(5, 1))],
        [sg.Button('Connect', bind_return_key=True), sg.Button('List Connections'), sg.Button('Exit')]]

    window = sg.Window('Pomerium - BeyondCorp', layout, enable_close_attempted_event = True )
# WINDOW_CLOSE_ATTEMPTED_EVENT
    while True:  # Event Loop
        event, values = window.read()
        source = values['-IP-'] + ':' + values['-PORT-']

        #print(event, values)
        if event in (sg.WIN_CLOSED, 'Exit', sg.WINDOW_CLOSE_ATTEMPTED_EVENT):
            print('killing all pomerium tunnels')
            time.sleep(1)
            if 'Windows' in platform.system():
               CMD = 'taskkill /IM "pomerium-cli.exe" /F'
            elif 'Linux' in platform.system() or 'Darwin' in platform.system():
                CMD = 'pkill -f pomerium-cli'
            try:
              runCommand1(cmd=CMD, window=window)
            except:
                print('Failed to stop pomerium -- exiting')
            else:
                print('removing tunnel list:')
            try:
                f = open("connections.txt", "w")
                f.truncate()
                f.close()
            except:
                print('failed to clear file')
            else:
               print('cleared connection list, exiting')
               time.sleep(3)

            break
        elif event == 'Connect':
            #print(CMD)
            #sleep(5)
            if values['-IP-'].count('.') >= 2:
             try:
               val = int(values['-PORT-'])
             except ValueError:
               print(values['-PORT-'] + " is not an integer!")
             else:
               if int(values['-PORT-']) in range(0,65535):
                 port = find_free_port()
                 CMD = POM + ' ' + '--listen 127.0.0.1:' + str(port) + ' ' + source
                 try:
                   print(CMD)
                   runCommand1(cmd=CMD, window=window)
                 except:
                     sg.print(traceback.print_exc())
                     sg.popup('ERROR: Failed to open connection')
                 else:
                     sg.popup("Connect to: " + source + '\n' + 'ON: ' +  '127.0.0.1' + ':' + str(port))
                     f = open("connections.txt", "a")
                     f.write(source + ' ON: ' + ' 127.0.0.1' + ':' + str(port) + '\n')
                     f.close()
                     f = open("connections.txt", "r")
                     window.FindElement('-OUTPUT-').Update('')
                     Lines = f.read()
                     window['-OUTPUT-'].Update(Lines)
                     f.close
               else:
                   print(values['-PORT-'] + ' ' + 'Is an Invalid Port Number, please use a valid port number')
            else:
                print(values['-IP-'] + ' Is Not a valid IP or hostname Please input a valid IP or Hostname')
        elif event == 'List Connections':
            try: 
                f = open("connections.txt", "r")

            except:
                window['-OUTPUT-'].Update('No Connections Found')
            else:
                window.FindElement('-OUTPUT-').Update('')
                Lines = f.read()
                window['-OUTPUT-'].Update(Lines)
                f.close




def find_free_port():
       s = socket.socket()
       s.bind(('', 0))            # Bind to a free port provided by the host.
       return s.getsockname()[1]



def runCommand1(cmd, timeout=None, window=None):
    nop = None
    """ run shell command
    @param cmd: command to execute
    @param timeout: timeout for command execution
    @param window: the PySimpleGUI window that the output is going to (needed to do refresh on)
    @return: (return code from command, command output)
    """
    #print(CMD)

    try:
       p = subprocess.Popen(cmd, shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
    except:
        print('error in' + CMD)
        traceback.print_exc()





main()
