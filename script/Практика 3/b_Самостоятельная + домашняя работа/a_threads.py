"""
Модуль в котором содержаться потоки Qt
"""

import time
import requests
import psutil
from PySide6 import QtCore


class SystemInfo(QtCore.QThread):
    systemSignal = QtCore.Signal(list)

    # Создайте экземпляр класса Signal и передайте ему в конструктор тип данных
    # передаваемого значения (в текущем случае list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.delay = None

        self.status = True
        self.start()
        # создайте атрибут класса self.delay = None, для управлением задержкой получения данных

    def run(self) -> None:  # TODO переопределить метод run

        if self.delay is None:  # Если задержка не передана в поток перед его запуском
            self.delay = 1  # то устанавливайте значение 1
            self.status = False

        while self.status:  # Запустите бесконечный цикл получения информации о системе

            cpu_value = psutil.cpu_percent()  # с помощью вызова функции cpu_percent() в пакете psutil получите загрузку CPU
            ram_value = psutil.virtual_memory().percent  # с помощью вызова функции virtual_memory().percent в пакете psutil получите загрузку RAM
            data = []
            data.append(cpu_value)
            data.append(ram_value)
            print(data)
            self.systemSignal.emit(data)  # с помощью метода .emit передайте в виде списка данные о загрузке CPU и RAM
            time.sleep(self.delay)  # с помощью функции .sleep() приостановите выполнение цикла на время self.delay
            if self.delay == 0:
                self.status = False


class WeatherHandler(QtCore.QThread):
    # Пропишите сигналы, которые считаете нужными
    signalWeatherInfo = QtCore.Signal(dict)

    def __init__(self, lat, lon, parent=None):
        super().__init__(parent)

        self.__api_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        self.__delay = 10
        self.__status = None

    def setDelay(self, delay) -> None:
        """
        Метод для установки времени задержки обновления сайта

        :param delay: время задержки обновления информации о доступности сайта
        :return: None
        """

        self.__delay = delay

    def run(self) -> None:
        #  настройте метод для корректной работы
        if self.__delay == 0:  # если устанавливаем задержку > 0 то цикл будет работать
            self.__status = False

        else:
            self.__status = True

        while self.__status:

            response = requests.get(self.__api_url)

            data = (response.json())
            self.signalWeatherInfo.emit(data)
            time.sleep(self.__delay)

            if self.__delay == 0:  # если устанавливаем задержку > 0 то цикл будет работать
                self.__status = False


if __name__ == "__main__":
    pass
