"""
Реализовать виджет, который будет работать с потоком SystemInfo из модуля a_threads

Создавать форму можно как в ручную, так и с помощью программы Designer

Форма должна содержать:
1. поле для ввода времени задержки  ok
2. поле для вывода информации о загрузке CPU  ok
3. поле для вывода информации о загрузке RAM  ok
4. поток необходимо запускать сразу при старте приложения
5. установку времени задержки сделать "горячей", т.е. поток должен сразу
реагировать на изменение времени задержки
"""
import psutil

import a_threads
from PySide6 import QtWidgets, QtCore


class Intest_window(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._thread = a_threads.SystemInfo()
        self._thread.delay = 1

        self.initUI()

        self.__initSignal()

    def initUI(self):
        self.setWindowTitle('SystemInfo')
        self.setFixedSize(200, 220)
        self.labelBox = QtWidgets.QLabel("Введите время задержки")
        self.line_inpt_spinBox = QtWidgets.QSpinBox()
        self.line_inpt_spinBox.setValue(1)

        self.line_cpu_log = QtWidgets.QPlainTextEdit(str(self._thread.delay))
        self.line_ram_log = QtWidgets.QPlainTextEdit()

        self.pl_holderCPU = QtWidgets.QLabel()
        self.pl_holderCPU.setText("CPU:")
        self.pl_holderRAM = QtWidgets.QLabel("RAM:")

        layout_delay = QtWidgets.QVBoxLayout()
        layout_delay.addWidget(self.labelBox)
        layout_delay.addWidget(self.line_inpt_spinBox)

        layout_main1 = QtWidgets.QVBoxLayout()
        layout_main1.addLayout(layout_delay)
        layout_main1.addWidget(self.pl_holderCPU)
        layout_main1.addWidget(self.line_cpu_log)
        layout_main1.addWidget(self.pl_holderRAM)
        layout_main1.addWidget(self.line_ram_log)

        self.setLayout(layout_main1)

    def __initSignal(self):
        self.line_inpt_spinBox.valueChanged.connect(self.__delay_time_changed)
        self._thread.systemSignal.connect(
            lambda data: self._info(data))

    def _info(self, data: list):
        """ прописываем содержимое полученного из потока списка по ячейкам вывода информации"""
        self.line_cpu_log.appendPlainText(str(data[0]))
        self.line_ram_log.appendPlainText(str(data[1]))

    def __delay_time_changed(self):
        self._thread.delay = self.line_inpt_spinBox.value()

        if self._thread.isRunning() == False:
            self._thread.start()


if __name__ == "__main__":
    app = QtWidgets.QApplication()
    window = Intest_window()
    window.show()

    app.exec()
