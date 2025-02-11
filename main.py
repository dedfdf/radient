import requests
import sys
import os
from PyQt6 import QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton
from PyQt6.QtGui import QPixmap


api_key = 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13'
geo_api_key = '40d1649f-0493-4b70-98ba-98533de7710b'


class Window(QWidget):
    def __init__(self):
        self.z = 10
        self.params = {'ll': '37.617698,55.755864',
                       'size': '600,450',
                       'z': f'{self.z}',
                       'theme': 'light'}
        super().__init__()
        self.get_image()
        self.initUI()

    def get_image(self):
        response = requests.get(f'http://static-maps.yandex.ru/v1?apikey={api_key}',
                                params=self.params)
        if response:
            self.map_file = 'map.png'
            with open(self.map_file, 'wb') as file:
                file.write(response.content)
        else:
            print('Ошибка запроса!!')
            sys.exit(1)

    def initUI(self):
        self.setGeometry(0, 0, 515, 600)
        self.setWindowTitle('Карта')
        self.pixmap = QPixmap(self.map_file)
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(500, 500)
        self.image.setPixmap(self.pixmap)
        self.button = QPushButton('Тема', self)
        self.button.clicked.connect(self.smena_tema)
        self.button.move(0, 0)
        self.button.resize(50, 20)
        self.button.setStyleSheet("QPushButton {"
                                  "background-color: white;"
                                  "border: none;"
                                  "border-radius: 4px;}"
                                  "QPushButton:hover{background-color: gray}")
        self.flag = False

    def smena_tema(self):
        self.params = {'ll': '37.617698,55.755864',
                       'size': '600,450',
                       'z': f'{self.z}',
                       'theme': f'{"dark" if not self.flag else "light"}'}
        self.flag = not self.flag
        self.get_image()
        self.pixmap = QPixmap(self.map_file)
        self.image.setPixmap(self.pixmap)

    def keyPressEvent(self, event):
        if self.z + 1 != 21:
            if event.key() == Qt.Key.Key_PageUp:
                self.z += 1
                self.params = {'ll': '37.617698,55.755864',
                          'size': '600,450',
                          'z': f'{self.z}'}
                self.get_image()
                self.pixmap = QPixmap(self.map_file)
                self.image.setPixmap(self.pixmap)
        if self.z - 1 != 0:
            if event.key() == Qt.Key.Key_Down:
                self.z -= 1
                self.params = {'ll': '37.617698,55.755864',
                          'size': '600,450',
                          'z': f'{self.z}'}
                self.get_image()
                self.pixmap = QPixmap(self.map_file)
                self.image.setPixmap(self.pixmap)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())

