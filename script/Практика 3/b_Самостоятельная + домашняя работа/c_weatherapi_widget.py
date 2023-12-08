"""
Реализовать виджет, который будет работать с потоком WeatherHandler из модуля a_threads

Создавать форму можно как в ручную, так и с помощью программы Designer

Форма должна содержать:
1. поле для ввода широты и долготы (после запуска потока они должны блокироваться)
2. поле для ввода времени задержки (после запуска потока оно должно блокироваться)
3. поле для вывода информации о погоде в указанных координатах
4. поток необходимо запускать и останавливать при нажатие на кнопку
"""
import time
import requests
from PySide6 import QtWidgets, QtCore
# from form_weather import Ui_FormWeather
import a_threads


class WindowWeather(QtWidgets.QWidget):

    def __init__(self, lat=None, lon=None, parent=None):
        super().__init__(parent)
        if lat is lat or lon is None:
            self.lat = 36.826903
            self.lon = 10.173742
        else:
            self.lat = float(lat)
            self.lon = float(lon)

        self._initUI_weather()
        self.update_coord()
        self.init_Signal()

    def _initUI_weather(self):
        self.WeatherHandler = a_threads.WeatherHandler(self.lat, self.lon)

        labelH_lay = QtWidgets.QHBoxLayout()
        coordH_lay = QtWidgets.QHBoxLayout()

        self.delay_inpt_spinBox = QtWidgets.QSpinBox()
        self.delay_inpt_spinBox.setValue(10)

        self.line_lattitude = QtWidgets.QLineEdit()
        self.line_long = QtWidgets.QLineEdit()
        self.line_long.setClearButtonEnabled(True)
        self.line_lattitude.setClearButtonEnabled(True)

        self.lat_label = QtWidgets.QLabel("lattitude")
        self.lon_label = QtWidgets.QLabel("longitude")

        labelH_lay.addWidget(self.lat_label)
        labelH_lay.addWidget(self.lon_label)

        coordH_lay.addWidget(self.line_lattitude)
        coordH_lay.addWidget(self.line_long)

        self.info_log = QtWidgets.QPlainTextEdit()
        self.info_label = QtWidgets.QLabel("Метео инфо")
        self.push_but = QtWidgets.QPushButton("Do it")
       # self.push_but.initStyleOption()
        self.push_but.setStyleSheet("background-color: blue; border: 4px solid red; border-radius : 10px")

        info_layout = QtWidgets.QHBoxLayout()
        info_layout.addWidget(self.info_label)
        info_layout.addWidget(self.delay_inpt_spinBox)

        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.addLayout(labelH_lay)
        self.main_layout.addLayout(coordH_lay)
        self.main_layout.addLayout(info_layout)
        self.main_layout.addWidget(self.info_log)

        self.main_layout.addWidget(self.push_but)
        self.push_but.setDefault(True)

        self.setLayout(self.main_layout)

    def init_Signal(self):
        self.push_but.clicked.connect(self.push_but_clicked)
        self.delay_inpt_spinBox.valueChanged.connect(self.WeatherHandler.setDelay(self.delay_inpt_spinBox.value()))

    def update_coord(self):
        self.line_lattitude.setText(str(self.lat))
        self.line_long.setText(str(self.lon))

    def push_but_clicked(self):
        if self.push_but.text() == "Do it":  # включаем поток
            if self.validate_data():
                if self.delay_inpt_spinBox.value() > 0:
                    self._init_visibility()
                    self.WeatherHandler.setDelay(self.delay_inpt_spinBox.value())
                    self.WeatherHandler.start()
                    self.WeatherHandler.signalWeatherInfo.connect(lambda data: self.info_line_input(data))

        else:  # останавливаем поток

            self.WeatherHandler.setDelay(0)
            self._init_visibility()

    def info_line_input(self, data):
        info_data = data['current_weather']
        info_pref = data['current_weather_units']
        str_ = f"local data and time: {info_data['time']}\n" \
               f"temperature- {info_data['temperature']} {info_pref['temperature']}\n" \
               f"windspeed-{info_data['windspeed']}{info_pref['windspeed']} winddirection-{info_data['winddirection']}\n"
        self.info_log.appendPlainText(str_)

    def validate_data(self):
        lat_text = self.line_lattitude.text()
        long_text = self.line_long.text()
        try:
            lat_float = float(lat_text)
            long_float = float(long_text)
            if -180 <= lat_float <= 180:
                self.line_lattitude.setStyleSheet("")
                self.lat = lat_float
            else:
                self.line_lattitude.setStyleSheet("background-color: red;")
                self.info_log.setPlainText('Введите корректные координат')
                return False

            if -180 <= long_float <= 180:
                self.line_long.setStyleSheet("")
                self.lon = long_float

            else:
                self.line_long.setStyleSheet("background-color: red;")
                self.info_log.setPlainText('Введите корректные координаты')
                return False
            return True

        except ValueError:
            self.line_lattitude.setStyleSheet("background-color: red;")
            self.line_long.setStyleSheet("background-color: red;")
            self.info_log.setPlainText("Введите корректные координаты")
            return False

    def _init_visibility(self):
        if self.push_but.text() == "Do it":
            self.line_lattitude.setReadOnly(True)
            self.line_long.setReadOnly(True)
            self.line_lattitude.setStyleSheet("background-color: yellow")
            self.line_long.setStyleSheet("background-color: yellow")
            self.push_but.setText("Stop it")
            self.delay_inpt_spinBox.setReadOnly(True)
        else:
            self.line_lattitude.setReadOnly(False)
            self.line_long.setReadOnly(False)
            self.line_lattitude.setStyleSheet("background-color: white")
            self.line_long.setStyleSheet("background-color: white")
            self.delay_inpt_spinBox.setReadOnly(False)
            self.push_but.setText("Do it")


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = WindowWeather()
    window.show()

    app.exec()
