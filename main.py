import requests
import sys
import os
from PyQt6.QtWidgets import QApplication, QWidget, QLabel
from PyQt6.QtGui import QPixmap

api_key = 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13'
geo_api_key = '40d1649f-0493-4b70-98ba-98533de7710b'


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.get_image()
        self.initUI()

    def get_image(self):
        response = requests.get(f'http://static-maps.yandex.ru/v1?apikey={api_key}&ll=37.617698,55.755864&lang=ru_RU&pt=37.439194,55.81782~37.55787,55.711939~37.559353,55.791137&size=450,450&z=10')
        if response:
            self.map_file = 'map.png'
            with open(self.map_file, 'wb') as file:
                file.write(response.content)
        else:
            print('Ошибка запроса!!')
            sys.exit(1)

    def initUI(self):
        self.setGeometry(300, 300, 500, 500)
        self.setWindowTitle('Карта')
        self.pixmap = QPixmap(self.map_file)
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(500, 500)
        self.image.setPixmap(self.pixmap)

    def closeEvent(self, event):
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())

