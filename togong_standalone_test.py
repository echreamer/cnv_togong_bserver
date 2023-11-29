from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5.QtCore import Qt
import socket
import sys
import json



def test():
    try:
        data = {
                    "type": "test",
                    "message": 2
                }

        # JSON으로 직렬화
        json_data = json.dumps(data)

        # 소켓 설정 및 연결
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('localhost', 9989))

        # JSON 데이터 전송
        client_socket.sendall(json_data.encode('utf-8'))
        client_socket.close()






    except Exception as e:
        print(f"Error:{e}")






class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.button = QPushButton("TEST",self)
        self.button.clicked.connect(test)
        self.button.resize(300,100)
        self.button.move(50,50)

        self.setWindowTitle("Blender Connection Test")
        self.setGeometry(500,500,500,500)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)




def main():
    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec_())




if __name__ == "__main__":
    main()
