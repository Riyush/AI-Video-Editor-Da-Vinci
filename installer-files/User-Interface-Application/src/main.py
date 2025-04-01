from PyQt6 import QtWidgets, uic # Tool for building buttons, text, windows, etc

def simple_print():
    print("Hello from desktop app")
if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv) #Allows system related operations

    window = QtWidgets.QMainWindow()
    uic.loadUi('User-Interface-Application/src/file.ui', window)

    window.pushButton.clicked.connect(simple_print)
    window.show()

    sys.exit(app.exec())