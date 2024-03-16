# main_window.py
from PyQt5.QtWidgets import QMainWindow, QLabel, QLineEdit, QPushButton, QProgressBar, QMessageBox
from logic.youku_downloader import YoukuVideoDownloader

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("优酷视频下载和合并")
        self.setGeometry(100, 100, 500, 150)

        self.label = QLabel("请输入优酷的URL：", self)
        self.label.move(20, 20)

        self.lineEdit = QLineEdit(self)
        self.lineEdit.setGeometry(150, 20, 300, 30)

        self.button = QPushButton("下载视频", self)
        self.button.setGeometry(150, 100, 200, 30)
        self.button.clicked.connect(self.download_and_merge_video)


        self.downloader = YoukuVideoDownloader()  # 创建 YoukuVideoDownloader 实例

    def download_and_merge_video(self):
        url = self.lineEdit.text()

        def show_message(message, message_type):
            if message_type == "error":
                QMessageBox.critical(self, "错误", message)
            elif message_type == "success":
                QMessageBox.information(self, "成功", message)

        self.downloader.download_and_merge(url, show_message)
