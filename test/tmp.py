from time import sleep

from pynput import keyboard


class GetKey:

    def on_press(self, key):
        if "f8" in str(key):
            print(6)

    def start(self):
        self.listener = keyboard.Listener(on_press=self.on_press).start()


g = GetKey()
g.start()
sleep(30)
