from Elvis import *

from kivy.app import App
from kivy.uix.button import Button


class ElvisGuiInterface(App):
    def build(self):
        button = Button(text="Click to speak",
                        font_size="20sp",
                        background_color=(135, 0, 255, 0.8),
                        color=(1, 1, 1, 1),
                        size=(70, 100),
                        size_hint=(.2, .2),
                        pos=(320, 250))

        button.bind(on_press=self.runElvis)
        return button

    def runElvis(self, event):
        elvis = Elvis()
        elvis.greet()
        userVoiceCommand = elvis.getUserVoiceCommand()
        elvis.processCommand(userVoiceCommand)


##########################################################################################
if __name__ == "__main__":
    ElvisGuiInterface().run()

##########################################################################################
