from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets
import sys
from flask import Flask, render_template, request, url_for, redirect,jsonify
from flask_cors import CORS

import ocr
from bb import Blackboard
from ai import ChatBot
import sys

from threading import Thread
import requests
import pygame
import time
import os

import ast


finalPort = 1234


app = Flask(__name__)

cb = None

CORS(app)

isBlackboardOpen = False

PORT = None


def flaskapp(port):
    global PORT
    PORT = port
    app.run(port=PORT)

def launch_bb():

    b = Blackboard(f"localhost:{PORT}/")
    
    b.run()



@app.route('/fetch_resp', methods = ['GET', 'POST'])
def fetch_resp():
    global cb
    outs = ocr.rec_char()
    if cb is None:
        cb = ChatBot()
    resp = cb.msg(outs)
    print(resp)
    
    return str(resp)


@app.route('/aiCanvas_data', methods=['GET'])
def aiCanvas_data():
    
    global isBlackboardOpen
    
    if not isBlackboardOpen:
        isBlackboardOpen = True
        t_bb = Thread(target=launch_bb)
        t_bb.start()
        

    
        return render_template('aiCanvas_data.html', fetch='false', port=PORT)
    else:

        return render_template('aiCanvas_data.html', fetch='true', port=PORT)





@app.route('/blackboard_quit')#, methods=['GET'])
def blackboard_quit():
    global isBlackboardOpen
    
    if isBlackboardOpen:
        isBlackboardOpen = False
        
    print("quitting")
    return redirect(url_for("home"))


@app.route('/aiCanvas', methods=['GET'])
def aiCanvas():
    print(isBlackboardOpen)
    if isBlackboardOpen:
        return redirect(url_for("aiCanvas_data"))
    

    return render_template('aiCanvas.html', port=PORT)



@app.route('/testing')
def testing():
    return 'asjihdiohdua huei9wa eajsnjaiehw8 aihdajhw0d a90oaidji2ojeiojd aouw9-e a90uw09 assdhh'

@app.route('/')
def home():
    return render_template("base.html")

@app.route('/todolist')
def todolist():
    return render_template("ToDoList.html")

@app.route('/deadlines')
def deadlines():
    return render_template("deadlines.html")

@app.route('/flashcards')
def flashcards():
    return render_template("Flashcards.html")

@app.route('/aicanvas')
def aicanvas():
    return render_template("aiCanvas.html")

@app.route('/chemistry')
def chemistry():
    return render_template("chemistry.html")

@app.route('/electro')
def electro():
    return render_template("electro.html")

@app.route('/maths')
def maths():
    return render_template("maths.html")

@app.route('/physics')
def physics():
    return render_template("physics.html")

@app.route('/resources')
def resources():
    return render_template("Resources.html")

@app.route('/com')
def com():
    return render_template("COM.html")


def read_list_from_file(filename):
    try:
        with open(filename, 'r') as file:
            content = file.read()
            return ast.literal_eval(content)  # Convert the string back to a list
    except FileNotFoundError:
        return []

def write_list_to_file(filename, data_list):
    with open(filename, 'w') as file:
        file.write(str(data_list))  # Write the list as a string


# TO DO LIST
@app.route('/add_task', methods=['POST'])
def add_task():
    task = request.json.get('task')
    if task:
        tasks = read_list_from_file('tasks.txt')  # Read existing tasks from tasks.txt
        tasks.append(task)
        write_list_to_file('tasks.txt', tasks)  # Write updated tasks back to tasks.txt
        return jsonify({"success": True, "task": task}), 200
    return jsonify({"success": False}), 400

@app.route('/delete_task', methods=['POST'])
def delete_task():
    task = request.json.get('task')
    tasks = read_list_from_file('tasks.txt')  # Read existing tasks from tasks.txt
    if task in tasks:
        tasks.remove(task)
        write_list_to_file('tasks.txt', tasks)  # Write updated tasks back to tasks.txt
        return jsonify({"success": True}), 200
    return jsonify({"success": False}), 400

@app.route('/get_tasks', methods=['GET'])
def get_tasks():
    tasks = read_list_from_file('tasks.txt')  # Read tasks from tasks.txt
    return jsonify({"tasks": tasks}), 200

# DEADLINES
@app.route('/add_deadline', methods=['POST'])
def add_deadline():
    data = request.json
    event = data.get('event')
    datetime = data.get('datetime')
    if event and datetime:
        deadlines = read_list_from_file('deadlines.txt')  # Read existing deadlines from deadlines.txt
        deadlines.append({'event': event, 'datetime': datetime})
        write_list_to_file('deadlines.txt', deadlines)  # Write updated deadlines back to deadlines.txt
        return jsonify({"success": True, "deadline": {'event': event, 'datetime': datetime}}), 200
    return jsonify({"success": False}), 400

@app.route('/delete_deadline', methods=['POST'])
def delete_deadline():
    data = request.json
    event = data.get('event')
    deadlines = read_list_from_file('deadlines.txt')  # Read existing deadlines from deadlines.txt
    deadlines = [d for d in deadlines if d['event'] != event]
    print(deadlines)
    write_list_to_file('deadlines.txt', deadlines)  # Write updated deadlines back to deadlines.txt
    return jsonify({"success": True}), 200

@app.route('/get_deadlines', methods=['GET'])
def get_deadlines():
    deadlines = read_list_from_file('deadlines.txt')  # Read deadlines from deadlines.txt
    return jsonify(deadlines), 200

# FLASHCARDS
@app.route('/add_flashcard', methods=['POST'])
def add_flashcard():
    content = request.json.get('content')
    if content:
        flashcards = read_list_from_file('flashcards.txt')  # Read existing flashcards from flashcards.txt
        flashcards.append(content)
        write_list_to_file('flashcards.txt', flashcards)  # Write updated flashcards back to flashcards.txt
        return jsonify({"success": True, "flashcard": content}), 200
    return jsonify({"success": False}), 400

@app.route('/delete_flashcard', methods=['POST'])
def delete_flashcard():
    content = request.json.get('flashcard')
    if content:
        flashcards = read_list_from_file('flashcards.txt')  # Read existing flashcards from flashcards.txt
        if content in flashcards:
            flashcards.remove(content)
            write_list_to_file('flashcards.txt', flashcards)  # Write updated flashcards back to flashcards.txt
            return jsonify({"success": True}), 200
    return jsonify({"success": False}), 400

@app.route('/get_flashcards', methods=['GET'])
def get_flashcards():
    flashcards = read_list_from_file('flashcards.txt')  # Read flashcards from flashcards.txt
    return jsonify(flashcards), 200
    
    
class MainApp:
    
    finalport = None
    
    def run_server(self, port, alt_port, n):

        if n>4:
            print('Fatal: Port in use')
            sys.exit()
        
        serverStatus = None

        try:
            isServerRunning = requests.get(f'http://localhost:{port}/testing').text
            serverStatus = requests.get(f'http://localhost:{port}/testing').status_code
            print(serverStatus)
            print(isServerRunning)
        except ConnectionRefusedError:
            print('ConnRefErr')
            if not serverStatus:
                flaskapp(port=port)
                self.finalport = port
                print('port set')
                return
            
        
        except requests.exceptions.ConnectionError:
            print('ConErr')
            if not serverStatus:
                self.finalport = port
                print('port set')
                flaskapp(port=port)

                return
            

        
        except Exception as e:
            print(str(e))

            return
        

        try:
        
            if isServerRunning == 'asjihdiohdua huei9wa eajsnjaiehw8 aihdajhw0d a90oaidji2ojeiojd aouw9-e a90uw09 assdhh':
                print('Server is running')
                self.finalport = port
                print('port set')
                return
            
            if isServerRunning != 'asjihdiohdua huei9wa eajsnjaiehw8 aihdajhw0d a90oaidji2ojeiojd aouw9-e a90uw09 assdhh' or serverStatus == 404:
                print('Another application is running on the required port.')
                self.finalport = port
                print('port set')
                self.run_server(alt_port, port, n+1)
                
        except Exception as e:
            print(str(e))

            return
                
                
            
    def run_renderer(self):

        # try:            
        global app1
        app1 = QtWidgets.QApplication(['', '--no-sandbox'])

        self.MainWindow = Window(port=self.finalport)

        self.MainWindow.show()
        

        sys.exit(app1.exec_())

            # here
        # except Exception as e:
        #     print('e')
        #     print(str(e))
        

class Renderer(object):
    def __init__(self, MainWindow, port):
        super().__init__()
        
        screen = app1.primaryScreen()

        size = screen.size()

        rect = screen.availableGeometry()


        
        self.MainWindow = MainWindow
        self.MainWindow.setObjectName("Study Orbit")
        self.MainWindow.setWindowTitle("Study Orbit")
        self.MainWindow.resize(rect.width(), rect.height())
        self.MainWindow.setMinimumSize(800, 400)
        self.port = port
        print(self.port)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
     
        self.init_webView()

        
    def init_webView(self):
        
        self.webView = QtWebEngineWidgets.QWebEngineView(self.centralwidget)
        self.webView.setGeometry(QtCore.QRect(0, 0, self.MainWindow.frameGeometry().width(), self.MainWindow.frameGeometry().height()))
        self.webView.setUrl(QtCore.QUrl(f"http://localhost:{self.port}"))
        # self.webView.setUrl(QtCore.QUrl(f"https://google.com"))
        self.webView.page().profile().clearHttpCache()
        self.webView.setObjectName("webView")
        self.MainWindow.setCentralWidget(self.centralwidget)
        
    def resizeWebView(self):
        self.webView.setGeometry(QtCore.QRect(0, 0, self.MainWindow.frameGeometry().width(), self.MainWindow.frameGeometry().height()))



class Window(QtWidgets.QMainWindow):
    resized = QtCore.pyqtSignal()

    
    def  __init__(self, port):
        super().__init__()
        self.renderer = Renderer(MainWindow=self, port=port)

        
        self.resized.connect(lambda: self.renderer.resizeWebView())
        

    def resizeEvent(self, event):
        self.resized.emit()
        return None



class LoadingScreen:
    def __init__(self):
        self.exit_ = False
                        
        self.port = 5322
        self.alt_port = 1209

                        
        self.WIDTH = 400
        self.HEIGHT = 300
        self.FPS = 25
        
        pygame.init()

        self.clock = pygame.time.Clock()
        
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Study Orbit")
        
        self.frames = os.listdir('./loadingscreen')
        
        self.frames = self.sort_files(self.frames)

        
        self.no_frames = len(self.frames)
        
        self.runApp()
        
    
    def sort_files(self, files):
        sorted_files = []
        for i in files:
            num = int(i.split('_')[1])
            pair = (num, i)
            sorted_files.append(pair)
            
        sorted_files.sort(key=lambda x: x[0])

        return list(map(lambda x: x[1], sorted_files))

        
    def runApp(self):
        self.mainApp = MainApp()
        
        Thread(target=lambda: self.mainApp.run_server(self.port, self.alt_port, n=1), daemon=True).start()



    def bomb(self):
        time.sleep(5)
        self.exit_ = True
    
    
    def loadingScreen(self):
        bomb = Thread(target=self.bomb , daemon=True).start()

        curr_frame = 0
        while not self.exit_:
            self.clock.tick(self.FPS)
            if curr_frame == self.no_frames:
                curr_frame = 0
                
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
            self.screen.blit(pygame.image.load(f'./loadingscreen/{self.frames[curr_frame]}'), (0, 0))
            
            curr_frame+=1
            pygame.display.update()       



# try:
ls = LoadingScreen()
ls.loadingScreen()
# except:
#     pass

pygame.quit()

ls.mainApp.run_renderer()

def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)

if __name__ == "__main__":

    import sys
    sys.excepthook = except_hook
