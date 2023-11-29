"""
Реализация программу взаимодействия виджетов друг с другом:
Форма для приложения (ui/d_eventfilter_settings.ui)

Программа должна обладать следующим функционалом:

1. Добавить для dial возможность установки значений кнопками клавиатуры(+ и -),
   выводить новые значения в консоль

2. Соединить между собой QDial, QSlider, QLCDNumber
   (изменение значения в одном, изменяет значения в других)

3. Для QLCDNumber сделать отображение в различных системах счисления (oct, hex, bin, dec),
   изменять формат отображаемого значения в зависимости от выбранного в comboBox параметра.

4. Сохранять значение выбранного в comboBox режима отображения
   и значение LCDNumber в QSettings, при перезапуске программы выводить
   в него соответствующие значения
"""

from PySide6 import QtWidgets, QtCore
from ui.ui_ev_filtr import Ui_Form

from PySide6.QtGui import QKeyEvent


class Window(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.__load()

        self.__initSignal()


    def __load(self):
        initial_set = QtCore.QSettings("initialSetApp")
        self.combo_index = initial_set.value("lcd_index", 0)
        self.value = initial_set.value("index", 0)
        self.ui.dial.setValue(self.value)
        self.ui.horizontalSlider.setValue(self.value)
        self._initCombo()

       # self._LCD_()
    def __save(self):
        save_settings =  QtCore.QSettings("initialSetApp")
        save_settings.setValue("lcd_index", self.combo_index)
        save_settings.setValue("index", self.value)

    def __initSignal(self):
        self.ui.comboBox.currentIndexChanged.connect(self._comboBoxIndCh)
        self.ui.dial.valueChanged.connect(self.__dialValueChanged)
        self.ui.horizontalSlider.valueChanged.connect(self.__sliderValueChanged)
      #  print(QKeyEvent.key())

    def keyPressEvent(self, event: QKeyEvent):

        if event.key() == QtCore.Qt.Key_Plus:
            self.value += 1
         #   print("ok +", self.value)
        elif event.key() == QtCore.Qt.Key_Minus:
            self.value -= 1
         #   print("ok -", self.value)

        self.ui.horizontalSlider.setValue(self.value)
        self.ui.dial.setValue(self.value)
        self._LCD_()

        return super(Window, self).keyPressEvent(event)

    def __sliderValueChanged(self):
        self.value = self.ui.horizontalSlider.value()
        self.ui.dial.setValue(self.value)
        self._LCD_()

    def __dialValueChanged(self):
        self.value = self.ui.dial.value()
        self.ui.horizontalSlider.setValue(self.value)
        self._LCD_()


    def _comboBoxIndCh(self):

        if self.ui.comboBox.currentIndex() == 0: #"dec"
            self.ui.lcdNumber.setDecMode()
        elif self.ui.comboBox.currentIndex() == 1:# "oct"
            self.ui.lcdNumber.setOctMode()
        elif self.ui.comboBox.currentIndex() == 2:  #"hex"  oct, hex, bin, dec
            self.ui.lcdNumber.setHexMode()
        elif self.ui.comboBox.currentIndex() == 3:  # bin, dec
            self.ui.lcdNumber.setBinMode()
        self.combo_index = self.ui.comboBox.currentIndex()
        self._LCD_()

    def _initCombo(self):
        self.ui.comboBox.insertItem(0, "dec")
        self.ui.comboBox.insertItem(1, "oct")
        self.ui.comboBox.insertItem(2, "hex")
        self.ui.comboBox.insertItem(3,"bin")
        t = self.ui.comboBox.currentIndex()
        self.ui.comboBox.setCurrentIndex(self.combo_index)
        self._comboBoxIndCh()



    def _LCD_(self):

        self.ui.lcdNumber.display(self.value)
        self.__save()
        #self.ui.dial.rangeChanged
        #self.ui.dial.sliderMoved



if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()
