import paramiko
import tkinter as tk

# Set up the SSH client
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

def connect():
    # Connect to the remote computer
    ssh.connect('192.168.100.114', username='daniel', key_filename='/home/daniel/.ssh/id_rsa')

def disconnect():
    # Close the SSH connection
    ssh.close()

def run_script():
    # Execute a command on the remote computer
    stdin, stdout, stderr = ssh.exec_command('python3 emotions_tflite.py')

    # Print the output of the command
    print(stdout.read().decode())

# Create the main window
root = tk.Tk()
root.title("Remote Script Manager")

# Create the buttons
connect_button = tk.Button(root, text="Connect", command=connect)
connect_button.pack()

run_button = tk.Button(root, text="Run Script", command=run_script)
run_button.pack()

disconnect_button = tk.Button(root, text="Disconnect", command=disconnect)
disconnect_button.pack()

# Run the main loop
root.mainloop()

