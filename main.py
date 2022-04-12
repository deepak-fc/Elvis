from elvis import *

import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.core.window import Window

Builder.load_file('elvis_design.kv')


class MainWidget(Widget):
    def runElvis(self):
        elvis = Elvis()
        elvis.greet()
        userVoiceCommand = elvis.getUserVoiceCommand()
        elvis.processCommand(userVoiceCommand)


class ElvisApplication(App):
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        return MainWidget()


##########################################################
if __name__ == '__main__':
    ElvisApplication().run()
