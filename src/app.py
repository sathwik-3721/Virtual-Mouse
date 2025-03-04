import eel
import os
from queue import Queue

class ChatBot:

    started = False
    userinputQueue = Queue()

    @staticmethod
    def isUserInput():
        return not ChatBot.userinputQueue.empty()

    @staticmethod
    def popUserInput():
        return ChatBot.userinputQueue.get()

    @staticmethod
    def close_callback(route, websockets):
        if not websockets:
            print('GUI Closed!')
            ChatBot.close()
            exit()

    @staticmethod
    @eel.expose
    def getUserInput(msg):
        ChatBot.userinputQueue.put(msg)
        print(f"User Input: {msg}")
    
    @staticmethod
    def close():
        ChatBot.started = False

    @staticmethod
    def addUserMsg(msg):
        eel.addUserMsg(msg)
    
    @staticmethod
    def addAppMsg(msg):
        eel.addAppMsg(msg)

    @staticmethod
    def start():
        path = os.path.dirname(os.path.abspath(__file__))
        eel.init(os.path.join(path, 'web'), allowed_extensions=['.js', '.html'])
        try:
            print("Starting GUI Window...")
            eel.start('index.html', mode='chrome',
                      host='localhost',
                      port=27005,
                      block=False,
                      size=(350, 480),
                      position=(10, 100),
                      disable_cache=True,
                      close_callback=ChatBot.close_callback)
            ChatBot.started = True
            print("GUI Window Started...")
            while ChatBot.started:
                try:
                    eel.sleep(10.0)
                except Exception as e:
                    print(f"Exception occurred: {e}")
                    break
        except Exception as e:
            print(f"Failed to start GUI: {e}")
            pass
