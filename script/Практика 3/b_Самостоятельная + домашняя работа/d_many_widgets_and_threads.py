"""
Реализовать окно, которое будет объединять в себе сразу два предыдущих виджета
"""
import psutil
import time
import requests
from PySide6 import QtWidgets, QtCore

import a_threads
import b_systeminfo_widget

import c_weatherapi_widget


class Complex_window(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._thread = a_threads.SystemInfo()
        self._thread.delay = 3

        self.lat = 36.826903
        self.lon = 10.173742
        self.WeatherHandler = a_threads.WeatherHandler(self.lat, self.lon)

        self.initUI_weather()
        self.initUI_system()
        self.update_coord()
        self.initUI()

        #  self.__initSignal()
        self.init_Signal()

    def init_Signal(self):
        self.delay_inpt_spinBox.valueChanged.connect(self._delay_time_changed)

        self._thread.systemSignal.connect(
            lambda data: self._info(data))

        self.push_but.clicked.connect(self.push_but_clicked)

    #   self.push_but.clicked.connect(print("doit"))

    def _info(self, data: list):
        """ прописываем содержимое полученного из потока списка по ячейкам вывода информации"""
        self.line_cpu_log.appendPlainText(str(data[0]))
        self.line_ram_log.appendPlainText(str(data[1]))

    def _delay_time_changed(self):
        new_delay_value = self.delay_inpt_spinBox.value()
        self.WeatherHandler.setDelay(new_delay_value)
        self._thread.setDelay(new_delay_value)


        if self._thread.isRunning() == False:
            self._thread.start()

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
            self.push_but.setText("Stop it")
        #       self.delay_inpt_spinBox.setReadOnly(True)
        else:
            self.line_lattitude.setReadOnly(False)
            self.line_long.setReadOnly(False)
            #        self.delay_inpt_spinBox.setReadOnly(False)
            self.push_but.setText("Do it")

    def initUI_weather(self):

        labelH_lay = QtWidgets.QHBoxLayout()
        coordH_lay = QtWidgets.QHBoxLayout()

        self.delay_inpt_spinBox = QtWidgets.QSpinBox()
        self.delay_inpt_spinBox.setValue(3)

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

        info_layout = QtWidgets.QHBoxLayout()
        info_layout.addWidget(self.info_label)
        #  info_layout.addWidget(self.delay_inpt_spinBox)

        self.weather_main_layout = QtWidgets.QVBoxLayout()
        self.weather_main_layout.addLayout(labelH_lay)
        self.weather_main_layout.addLayout(coordH_lay)
        self.weather_main_layout.addLayout(info_layout)
        self.weather_main_layout.addWidget(self.info_log)

        #   self.weather_main_layout.addWidget(self.push_but)
        self.push_but.setDefault(True)

    def initUI_system(self):

        self.labelBox = QtWidgets.QLabel("Введите время задержки")
        self.line_inpt_spinBox = QtWidgets.QSpinBox()
        self.line_inpt_spinBox.setValue(3)

        self.line_cpu_log = QtWidgets.QPlainTextEdit()
        self.line_ram_log = QtWidgets.QPlainTextEdit()
        self.line_ram_log.setFixedHeight(50)
        self.line_cpu_log.setFixedHeight(50)

        self.pl_holderCPU = QtWidgets.QLabel()
        self.pl_holderCPU.setText("CPU:")
        self.pl_holderRAM = QtWidgets.QLabel("RAM:")

        layout_delay = QtWidgets.QVBoxLayout()
        layout_delay.addWidget(self.labelBox)
        #   layout_delay.addWidget(self.line_inpt_spinBox)

        self.layout_main_sys = QtWidgets.QVBoxLayout()

        self.layout_main_sys.addWidget(self.pl_holderCPU)
        self.layout_main_sys.addWidget(self.line_cpu_log)
        self.layout_main_sys.addWidget(self.pl_holderRAM)
        self.layout_main_sys.addWidget(self.line_ram_log)
        self.layout_main_sys.addLayout(layout_delay)

    def initUI(self):
        self._layout_comlex = QtWidgets.QVBoxLayout()
        self._layout_comlex.addLayout(self.weather_main_layout)
        self._layout_comlex.addLayout(self.layout_main_sys)
        self._layout_comlex.addWidget(self.delay_inpt_spinBox)
        self._layout_comlex.addWidget(self.push_but)

        self.setLayout(self._layout_comlex)

    def update_coord(self):
        self.line_lattitude.setText(str(self.lat))
        self.line_long.setText(str(self.lon))


if __name__ == "__main__":
    app = QtWidgets.QApplication()
    window1 = Complex_window()
    window1.show()

    app.exec()
