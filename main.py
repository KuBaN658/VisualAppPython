import json
import sys
import datetime
import requests


from PyQt6 import uic, QtCore, QtGui, QtWidgets


class MainWindow(QtWidgets.QMainWindow):
    ServerAddress = "http://127.0.0.1:5000/"
    MessageID = 0

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        uic.loadUi('messanger.ui', self)
        self.button.clicked.connect(self.pushButton1_clicked)

    def pushButton1_clicked(self):
        self.SendMessage()

    def SendMessage(self):
        user_name = self.username.text()
        message_text = self.message.text()
        timestamp = str(datetime.datetime.today())
        msg = f"{{\"UserName\": \"{user_name}\", \"MessageText\": \"{message_text}\", \"TimeStamp\": \"{timestamp}\"}}"
        # {"UserName": "RusAl", "MessageText": "Privet na sto let!!!", "TimeStamp": "2021-03-05T18:23:10.932973Z"}
        print("Отправлено сообщение: " + msg)
        url = self.ServerAddress + "api/Messanger"
        data = json.loads(msg)  # string to json
        r = requests.post(url, json=data)
        # print(r.status_code, r.reason)



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())
