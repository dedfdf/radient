import requests
import sys
import os
from PyQt6 import QtCore
from PyQt6.QtCore import Qt, QEvent
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit, QRadioButton
from PyQt6.QtGui import QPixmap


api_key = 'dda3ddba-c9ea-4ead-9010-f43fbc15c6e3'
api_server = 'https://static-maps.yandex.ru/v1'
geo_api_server = 'https://geocode-maps.yandex.ru/1.x'


class Window(QWidget):
    def __init__(self):
        self.z = 8
        self.ll = ['-71.699362', '18.873402']
        self.params = {'ll': f'{self.ll[0]},{self.ll[1]}',
                       'size': '600,450',
                       'z': f'{self.z}',
                       'theme': 'light',
                       'apikey': '5e15c6e4-9287-4e62-8e19-2d6f8fa6c0df'
                       }
        super().__init__()
        self.get_image()
        self.initUI()

    def get_image(self):
        response = requests.get(api_server, params=self.params)
        if response:
            self.map_file = 'map.png'
            with open(self.map_file, 'wb') as file:
                file.write(response.content)
        else:
            print('Ошибка запроса!!')
            sys.exit(1)

    def initUI(self):
        self.pt = []
        self.setGeometry(0, 0, 500, 700)
        self.setWindowTitle('Карта')
        self.pixmap = QPixmap(self.map_file)
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(500, 500)
        self.image.setPixmap(self.pixmap)
        self.button = QPushButton('Тема', self)
        self.button.clicked.connect(self.smena_tema)
        self.button.move(0, 2)
        self.button.resize(50, 20)
        self.button.setStyleSheet("QPushButton {"
                                  "background-color: white;"
                                  "border: none;"
                                  "border-radius: 4px;}"
                                  "QPushButton:hover{background-color: gray}")
        self.theme = 'light'
        self.request_field = QLineEdit(self)
        self.request_field.setPlaceholderText('Введите адрес')
        self.request_field.move(0, 480)
        self.request_field.resize(300, 35)
        self.request_field.installEventFilter(self)

        self.request_button = QPushButton('Искать', self)
        self.request_button.move(310, 480)
        self.request_button.resize(70, 35)
        self.request_button.clicked.connect(self.new_adres)
        self.request_button.installEventFilter(self)

        self.reset = QPushButton('Сброс', self)
        self.reset.move(390, 480)
        self.reset.resize(70, 35)
        self.reset.clicked.connect(self.sbros)
        self.reset.installEventFilter(self)

        self.adres_field = QLineEdit(self)
        self.adres_field.setPlaceholderText('Адрес найденного объекта')
        self.adres_field.setEnabled(False)
        self.adres_field.move(0, 525)
        self.adres_field.resize(460, 35)

        self.pocht_adres_field = QLineEdit(self)
        self.pocht_adres_field.setPlaceholderText('Почтовый индекс найденного объекта')
        self.pocht_adres_field.setEnabled(False)
        self.pocht_adres_field.move(0, 570)
        self.pocht_adres_field.resize(460, 35)

        self.on_pocht_adres = QRadioButton('Включить отображение почтового индекса', self)
        self.on_pocht_adres.move(0, 615)
        self.on_pocht_adres.clicked.connect(self.display_pocht_adres_field)
        self.off_pocht_adres = QRadioButton('Выключить отображение почтового индекса', self)
        self.off_pocht_adres.move(0, 645)
        self.off_pocht_adres.clicked.connect(self.display_pocht_adres_field)
        self.on_pocht_adres.installEventFilter(self)
        self.off_pocht_adres.installEventFilter(self)


    def eventFilter(self, source, event):
        if event.type() == QEvent.Type.KeyPress:
            if (event.key() == Qt.Key.Key_Down or event.key() == Qt.Key.Key_Left or
                    event.key() == Qt.Key.Key_Up or event.key() == Qt.Key.Key_Right):
                self.check_arrow(event)
                self.update()
        return super().eventFilter(source, event)


    def display_pocht_adres_field(self):
        if self.on_pocht_adres.isChecked():
            self.pocht_adres_field.show()
        else:
            self.pocht_adres_field.hide()

    def sbros(self):
        geo_params = {
            'apikey': 'd550bbbe-364a-4a39-aab1-e9882836aa1b',
            'geocode': str(self.request_field.text()),
            'format': 'json'
        }
        response = requests.get(geo_api_server, params=geo_params)
        if response:
            json_response = response.json()
            if len(json_response["response"]["GeoObjectCollection"]["featureMember"]) >= 1:
                toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
                coords = toponym['Point']['pos'].split()
                last_pt = f'{coords[0]},{coords[1]},pm2rdm'
                if last_pt in self.pt:
                    del self.pt[self.pt.index(last_pt)]
                self.adres_field.setText('')
                self.request_field.setText('')
                self.update()


    def update(self):
        self.params = {'ll': f'{self.ll[0]},{self.ll[1]}',
                       'size': '600,450',
                       'z': f'{self.z}',
                       'theme': self.theme,
                        'pt': '~'.join(self.pt),
                       'apikey': '5e15c6e4-9287-4e62-8e19-2d6f8fa6c0df'
                    }
        self.get_image()
        self.pixmap = QPixmap(self.map_file)
        self.image.setPixmap(self.pixmap)

    def new_adres(self):
        geo_params = {
            'apikey': 'd550bbbe-364a-4a39-aab1-e9882836aa1b',
            'geocode': str(self.request_field.text()),
            'format': 'json'
        }
        response = requests.get(geo_api_server, params=geo_params)
        if response:
            json_response = response.json()
            if len(json_response["response"]["GeoObjectCollection"]["featureMember"]) >= 1:

                toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
                coords = toponym['Point']['pos']
                self.ll = coords.split()
                new_pt = f'{self.ll[0]},{self.ll[1]},pm2rdm'
                if new_pt not in self.pt:
                    self.pt.append(new_pt)

                self.pocht_adres_field.setText(json_response["response"]["GeoObjectCollection"]["featureMember"][0]['GeoObject']['metaDataProperty']['GeocoderMetaData']['Address']['postal_code'])
                self.adres_field.setText(json_response["response"]["GeoObjectCollection"]["featureMember"][0]['GeoObject']['metaDataProperty']['GeocoderMetaData']['text'])

                self.update()

    def smena_tema(self):
        self.theme = "dark" if self.theme == 'light' else "light"
        self.update()

    def check_arrow(self, event):
        if self.z <= 21 and self.z >= 17:
            k = self.z / 100000
        elif self.z < 17 and self.z >= 14:
            k = self.z / 5000
        elif self.z < 14 and self.z >= 10:
            k = self.z / 700
        elif self.z < 10 and self.z >= 5:
            k = self.z / 20
        else:
            k = self.z * 2
        if event.key() == Qt.Key.Key_Down:
            if float(self.ll[1]) - k >= -84.77659799999994:
                self.ll[1] = str(float(self.ll[1]) - k)
        elif event.key() == Qt.Key.Key_Left:
            if float(self.ll[0]) - k >= -180:
                self.ll[0] = str(float(self.ll[0]) - k)
        elif event.key() == Qt.Key.Key_Up:
            if float(self.ll[1]) + k <= 84.77659799999994:
                self.ll[1] = str(float(self.ll[1]) + k)
        elif event.key() == Qt.Key.Key_Right:
            if float(self.ll[0]) + k <= 180:
                self.ll[0] = str(float(self.ll[0]) + k)


    def keyPressEvent(self, event):
        if self.z + 1 != 21:
            if event.key() == Qt.Key.Key_PageUp:
                self.z += 1
        if self.z - 1 != 0:
            if event.key() == Qt.Key.Key_PageDown:
                self.z -= 1
        self.check_arrow(event)
        self.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())

