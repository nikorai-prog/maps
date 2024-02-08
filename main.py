import os
import sys

import requests
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from main_menu import Ui_Form
from PyQt5 import QtWidgets

SCREEN_SIZE = [600, 450]
zoom = 0.005


class MainMenu(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.run)

    def run(self, x=None, y=None, delta=None):
        if not x and not y and not delta:
            x, y, delta = float(self.doubleSpinBox.text().replace(',', '.')),\
                          float(self.doubleSpinBox_2.text().replace(',', '.')),\
                          float(self.doubleSpinBox_3.text().replace(',', '.'))
        self.ex1 = Example(x, y, delta)
        self.ex1.show()


class Example(QWidget):
    def __init__(self, x, y, delta):
        super().__init__()
        self.x = x
        self.y = y
        self.delta = delta
        self.getImage()
        self.initUI()
        print(self.delta)

    def getImage(self):
        map_request = f"http://static-maps.yandex.ru/1.x/?ll={self.x},{self.y}&spn={self.delta},{self.delta}&l=map"
        response = requests.get(map_request)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        # Запишем полученное изображение в файл.
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')

        ## Изображение
        self.pixmap = QPixmap(self.map_file)
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.image.setPixmap(self.pixmap)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_PageUp:
            if self.delta + zoom < 100:
                self.delta += zoom
            ex.run(self.x, self.y, self.delta)
        elif event.key() == QtCore.Qt.Key_PageDown:
            if self.delta - zoom > 0:
                self.delta -= zoom
            ex.run(self.x, self.y, self.delta)
        event.accept()

    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainMenu()
    ex.show()
    sys.exit(app.exec())