from Elvis import *

##########################################################################################
if __name__ == "__main__":
    elvis = Elvis()
    elvis.greet()
    while True:
        userVoiceCommand = elvis.getUserVoiceCommand()
        elvis.processCommand(userVoiceCommand)

##########################################################################################
