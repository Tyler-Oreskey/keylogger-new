import threading
from pynput import keyboard

stop_listener_flag = threading.Event()
stop_malware_flag = threading.Event()
exit_program_flag = threading.Event()

def listener_thread():
    def on_key_release(key):
        global exit_program_flag
        if key == keyboard.Key.esc:
            exit_program_flag.set()
            return False

    with keyboard.Listener(
        on_press=lambda e : False,  # just return false
        on_release=on_key_release
        ) as listener:
        listener.join() # wait for listener thread to exit
        stop_listener_flag.set()

def malware_choice_listener_thread():
    def on_malware_key_release(key):
        global stop_malware_flag
        if key == keyboard.Key.esc:
            return False

    with keyboard.Listener(on_release=on_malware_key_release) as listener:
        listener.join()  # wait for listener thread to exit

# Main loop
while not stop_listener_flag.is_set():
    listener_thread_thread = threading.Thread(target=listener_thread)
    malware_choice_listener_thread_thread = threading.Thread(target=malware_choice_listener_thread)

    listener_thread_thread.start()
    listener_thread_thread.join()  # Wait for listener_thread to exit

    if exit_program_flag.is_set():
        break # exit loop when user presses escape

    if stop_listener_flag.is_set():
        # user chooses malware option
        malware_choice_listener_thread_thread.start()
        malware_choice_listener_thread_thread.join()  # Wait for malware_choice_listener_thread to exit