import PySimpleGUI as sg
import os.path
import paramiko
from scp import SCPClient
import os

# Set parameters
username = 'daniel'
ip = '192.168.100.113' 
public_key = '/home/daniel/.ssh/embe'
remote_dir = '/home/daniel/s1-2023/embebidos/p2/Emociones/'



# Set up the SSH client
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

def connect():
    # Connect to the remote computer
    ssh.connect(ip, username=username, key_filename=public_key)
    print("Connected successfully!")
def disconnect():
    # Close the SSH connection
    ssh.close()
    print("Disconnected successfully!")

def run_script():
    # Execute a command on the remote computer
    ssh.exec_command(f' source ~/anaconda3/etc/profile.d/conda.sh && conda activate base && cd {remote_dir} && nohup python emotions_pi.py &')

    # Print the output of the command
   # print(stderr.read().decode())
   # print(stdout.read().decode())
    print("Script ran successfully!")
def check_last_image():
    # Execute a command on the remote computer to get the last image in a folder
    folder_path = f'{remote_dir}capturas'
    cmd = f'ls -t {folder_path}/*.png | head -1'
    stdin, stdout, stderr = ssh.exec_command(cmd)
    last_image = stdout.read().decode().strip()
    # Copy the last image from the remote computer to the local computer using SCP
    
    local_dir = 'ultima_captura.png'
    local_path = os.path.join(os.getcwd(), local_dir)
    with SCPClient(ssh.get_transport()) as scp:
        scp.get(last_image, local_path)
    # Update the image displayed in the image_viewer_column
    window["-IMAGE-"].update(filename=local_path)
def emocion():
    # Execute a command on the remote computer to get the last word in the last line of a text file
    file_path = f'{remote_dir}output.csv'
    cmd = f'python3 -c "print(open(\'{file_path}\').readlines()[-1].split()[-1])"'
    stdin, stdout, stderr = ssh.exec_command(cmd)
    last_word = stdout.read().decode().strip()
    print(f'Emocion: {last_word}')
# First the window layout in 2 columns
def stop_script():
    ssh.exec_command('pkill -f emotions_pi.py')
    print("Script stopped successfully!")


def update_config_row_txt( row_num, new_values):
    # Read config data from file
    config_file = "config.txt"

    with open(config_file, 'r') as f:
        config_data = [line.strip() for line in f]

    # Update specified row with new values
    config_data[row_num] = new_values

    # Write updated config data to file
    with open(config_file, 'w') as f:
        for row in config_data:
            f.write(row + '\n')

def update_config_scp():
    # Set up SCP client
    scp = SCPClient(ssh.get_transport())

    # Set local and remote file paths
    local_file = 'config.txt'
    remote_file = f'{remote_dir}config.txt'

    # Transfer file from local to remote host
    scp.put(local_file, remote_file)

    # Close SCP and SSH connections
    scp.close()

def get_capturas():
    # Set up SCP client
    scp = SCPClient(ssh.get_transport())

    # Set remote and local directory paths
    remote_dir_C = f'{remote_dir}capturas'
    local_dir = 'capturas'

    # Transfer directory from remote to local host
    scp.get(remote_dir_c, local_dir, recursive=True)
    # Set remote and local file paths
    remote_file = f'{remote_dir}output.csv'
    local_file = 'output.csv'

    # Transfer file from remote to local host
    scp.get(remote_file, local_file)
    # Close SCP and SSH connections
    scp.close()

file_list_column = [
    [
            sg.Text("Image Folder"),
        sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
        sg.FolderBrowse(),
    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(40, 20), key="-FILE LIST-"
        )
    ],
]

# For now will only show the name of the file that was chosen
image_viewer_column = [
    [sg.Text("Choose an image from list on left:")],
    [sg.Text(size=(40, 1), key="-TOUT-")],
    [sg.Image(key="-IMAGE-")],
]

# ----- Full layout -----
layout = [
    [
        sg.Column(file_list_column),
        sg.VSeperator(),
        sg.Column(image_viewer_column),
    ],
    #[sg.Button('Connect', key='-CONNECT-')],
    [sg.Button('Run Script', key='-RUN-')],
    #[sg.Button('Disconnect', key='-DISCONNECT-')],
    [sg.Button('Update Photo', key='-UPDATE-')],
    [sg.Button('Stop program', key='-STOP-')],
    [sg.Text('Enter a value:'), sg.Input(key='input_value')],
    [sg.Button('Update Sample time'), sg.Button('Update max execution time'), sg.Button('Update max saved photos')],
    [sg.Button('Obtener capturas', key='-GET-')],
]

window = sg.Window("Image Viewer", layout)
try:
    connect()
except:
    print("No se pudo conectar con el dispositivo remoto")
# Run the Event Loop
while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    # Folder name was filled in, make a list of files in the folder
    if event == "-FOLDER-":
        folder = values["-FOLDER-"]
        try:
            # Get list of files in folder
            file_list = os.listdir(folder)
        except:
            file_list = []

        fnames = [
            f
            for f in file_list
            if os.path.isfile(os.path.join(folder, f))
            and f.lower().endswith((".png", ".gif",".jpg"))
        ]
        window["-FILE LIST-"].update(fnames)
    elif event == "-FILE LIST-":  # A file was chosen from the listbox
        try:
            filename = os.path.join(
                values["-FOLDER-"], values["-FILE LIST-"][0]
            )
            window["-TOUT-"].update(filename)
            window["-IMAGE-"].update(filename=filename)

        except:
            pass
    #elif event == '-CONNECT-':
    #    connect()
    elif event == '-RUN-':
        run_script()
    #elif event == '-DISCONNECT-':
    #    disconnect()
    elif event == '-UPDATE-':
        check_last_image()
        emocion()
    elif event == '-STOP-':
        stop_script()
    elif event == '-GET-':
        get_capturas()
    elif event == 'Update Sample time':
        input_value = values['input_value']
        #print(f'You entered: {input_value}')
        update_config_row_txt(0, input_value)
        update_config_scp()

    elif event == 'Update max execution time':
        input_value = values['input_value']
        #print(f'You entered: {input_value}')
        update_config_row_txt(1, input_value)
        update_config_scp()

    elif event == 'Update max saved photos':
        input_value = values['input_value']
        #print(f'You entered: {input_value}')
        update_config_row_txt(2, input_value)
        update_config_scp()

window.close()

