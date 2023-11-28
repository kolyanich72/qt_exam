"""
Реализация программу проверки состояния окна:
Форма для приложения (ui/c_signals_events.ui)

Программа должна обладать следующим функционалом:

1. Возможность перемещения окна по заданным координатам.  OK
2. Возможность получения параметров экрана (вывод производить в plainTextEdit + добавлять время).
    * Кол-во экранов                        OK
    * Текущее основное окно
    * Разрешение экрана                     OK
    * На каком экране окно находится
    * Размеры окна                          OK
    * Минимальные размеры окна              OK
    * Текущее положение (координаты) окна   OK
    * Координаты центра приложения     ??????????
    * Отслеживание состояния окна (свернуто/развёрнуто/активно/отображено)
3. Возможность отслеживания состояния окна (вывод производить в консоль + добавлять время).
    * При перемещении окна выводить его старую и новую позицию  OK
    * При изменении размера окна выводить его новый размер     OK
"""


from PySide6 import QtWidgets, QtCore, QtGui
import time


class Window(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.x_loc = QtWidgets.QLineEdit()
        self.y_loc = QtWidgets.QLineEdit()
        self.info_window = QtWidgets.QPlainTextEdit()
        x_cord = QtWidgets.QLabel()
        y_coord = QtWidgets.QLabel()
        x_cord.setText('X:')
        y_coord.setText('Y:')
        x_coord_l = QtWidgets.QHBoxLayout()
        y_coord_l =  QtWidgets.QHBoxLayout()
        self.x_loc.setPlaceholderText("по горизонтали")
        self.y_loc.setPlaceholderText("по вертикали")
        self.x_loc.setFixedSize(90, 25)
        self.y_loc.setFixedSize(90, 25)

        self.setMinimumSize(450, 450)
        x_coord_l.addWidget(x_cord)
        x_coord_l.addWidget(self.x_loc)
        x_coord_l.setAlignment(self.x_loc, QtCore.Qt.AlignLeft)


        y_coord_l.addWidget(y_coord)
        y_coord_l.addWidget(self.y_loc)
        y_coord_l.setAlignment(y_coord, QtCore.Qt.AlignRight)

        coordinate_bar = QtWidgets.QHBoxLayout()
        coordinate_bar.addLayout(x_coord_l)
        coordinate_bar.addLayout(y_coord_l)
        main_bar = QtWidgets.QVBoxLayout()
        self.info_window.setFixedSize(400,400)
        main_bar.addLayout(coordinate_bar)
        main_bar.addWidget(self.info_window)
        self.setLayout(main_bar)
        self.setVisible(True)
        self.x_loc.setText(str(self.x()))
        self.y_loc.setText(str(self.y()))
        self.__initSignals()

    def __initSignals(self):
        """Кол-во экранов  * Текущее основное окно   * Разрешение экрана
         * На каком экране окно находится"""
       # _screen_info = QtCore.QCoreApplication.instance().screens()
        q1 = QtCore.QCoreApplication.instance()
        screen1 = QtGui.QScreen()
        _screen_info = q1.screens()

        q2 = QtWidgets.QApplication
        q5= QtGui.QScreen.physicalDotsPerInchX(q2.screens()[0])
        q6 = QtGui.QScreen.physicalDotsPerInchY(q2.screens()[0])
        q7 = self.isHidden()
        q8 = self.isVisible()
        self.__signal(f"screen number-{len(_screen_info)}") #Кол-во экрано
        self.__signal(f'screen PixelRatio:{QtGui.QScreen.devicePixelRatio(q2.screens()[0])}') #Разрешение экрана
        self.__signal(f'screen size: {QtGui.QScreen.size(q2.screens()[0])}')   #Размер экрана
        self.__signal(f'screen physicalDotsPerInch: {q5} * {q6}') #Разрешение экрана
        self.__signal(f'window size : {self.size()}') #Размеры окна
        self.__signal(f'window min size : {self.minimumSize()}') #Минимальные размеры окна
        self.__signal(f'window position size : {self.pos()}')  # Текущее положение (координаты) окна
        self.__signal(f'window state : {self._window_current_state()}') # Отслеживание состояния окна
        self.__signal(f'window windowRole : {self.window().isActiveWindow()} {self.winId()}')
      #  self.__signal(f'window  : {q2.primaryScreen()}')
        self.x_loc.textChanged.connect(self._window_move)
        self.y_loc.textChanged.connect(self._window_move)

    def _window_move(self):
        try:
            x = int(self.x_loc.text())
        except:
            self.x_loc.setText("0")
        try:
            y = int(self.y_loc.text())
        except :
            self.y_loc.setText("0")
        # if not self.x_loc.text():
        #     self.x_loc.setText("0")
        # if not self.y_loc:
        #     self.y_loc.setText("0")
        self.move(int(self.x_loc.text()),int(self.y_loc.text()))



    def _window_current_state(self):# Отслеживание состояния окна (свернуто/развёрнуто/активно/отображено)
        data = "окно активно"
        if self.isHidden():
            data = "окно скрыто"
        elif self.isMinimized():
            data = "окно свернуто"
        elif self.isVisible():
            data = "окно отображено"
       # print("self.isHidden()", self.isHidden())
     #   print("self.isMinimized()", self.isMinimized())
     #   print("self.isVisible()", self.isVisible())
      #  print("self.isActiveWindow()", self.isActiveWindow())
     #   print("self.isEnabled()",self.isEnabled())
        return data

       # print(_screen_info, _screen_info_number)


    def __signal(self, data):
        self.info_window.appendPlainText(str(data))

        """Возможность отслеживания состояния окна (вывод производить в консоль + добавлять время).
    * При перемещении окна выводить его старую и новую позицию
    * При изменении размера окна выводить его новый размер"""

    def moveEvent(self, event: QtGui.QMoveEvent):
        print(f"old position:{event.oldPos()}, ,new position:{event.pos()}   time:{time.ctime()}")
        return super(Window, self).moveEvent(event)
    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        print(f"new size:{event}  time:{time.ctime()}")
        return super(Window, self).resizeEvent(event)


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()
