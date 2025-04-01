from PyQt6 import QtWidgets, uic # Tool for building buttons, text, windows, etc
import sys
import os

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        #Load the predesigned window design 
        # Get the directory of file.ui and then get file.ui
        # This setup works in development and production when I must get paths on user mac
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        ui_path = os.path.join(base_path, "file.ui")

        uic.loadUi(ui_path, self)

        #create a reference to the button object by going into the UI
        self.pushButton = self.findChild(QtWidgets.QPushButton, 'pushButton')

        # add button functionality upon a user click
        self.pushButton.clicked.connect(self.simple_print)


    def simple_print(self):
        print("Hello from desktop app")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv) #Allows system related operations

    window = MainWindow()
    window.show()

    sys.exit(app.exec())