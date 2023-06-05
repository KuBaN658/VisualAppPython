import json
import sys
import datetime
import requests


from PyQt6 import uic, QtCore, QtGui, QtWidgets
from urllib3.exceptions import HTTPError


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

    def GetMessage(self, id):
        id = str(id)
        url = self.ServerAddress + "/api/Messanger/" + id
        try:
            response = requests.get(url)
            response.raise_for_status()
        except HTTPError as http_err:
            print("Н")
            return None
        except Exception as err:
            return None
        else:
            text = response.text
            return text

    def timerEvent(self, msg):
        msg = self.GetMessage(self.MessageID)
        if msg is not None:
            msg = json.loads(msg)
            UserName = msg["UserName"]
            MessageText = msg["MessageText"]
            TimeStamp = msg["TimeStamp"]
            msgtext = f"{TimeStamp} : <{UserName}> : {MessageText}"
            #self.listMessages.insertItem(self.messageID, msgtext)
            self.MessageID += 1
            msg = self.GetMessage(self.MessageID)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    timer = QtCore.QTimer()
    time = QtCore.QTime(0, 0, 0)
    timer.timeout.connect(w.timerEvent)
    timer.start(5000)
    sys.exit(app.exec())
