import os
import sys
from PIL import Image

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor, QFont
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, \
    QFileDialog, QMessageBox, QMainWindow, QApplication


class LogoMixer(QWidget):
    def __init__(self):
        super().__init__()

        self.photo_path = ""
        self.logo_path = "logo/logo.png"

        self.input_frame = QLabel()
        self.input_frame.setMinimumSize(300, 200)
        v_box = QVBoxLayout()
        v_box.addStretch()

        v_box.addWidget(QLabel("Выберите папку с исходниками"))
        self.input_photo_path = QPushButton("Фото")
        self.input_photo_path.setFixedSize(300, 100)
        self.input_photo_path.setStyleSheet('QPushButton {background-color: darkblue}')
        self.input_photo_path.setFont(QFont('Impact', 15))
        self.input_photo_path.clicked.connect(self.get_photo_path)
        v_box.addWidget(self.input_photo_path)
        v_box.addStretch()

        v_box.addWidget(QLabel("Добавьте логотип на фотографии"))
        self.input_start = QPushButton("Старт")
        self.input_start.setFixedSize(300, 100)
        self.input_start.setStyleSheet('QPushButton {background-color: darkgreen}')
        self.input_start.setFont(QFont('Impact', 15))
        self.input_start.clicked.connect(self.add_photo_logo)
        v_box.addWidget(self.input_start)
        v_box.addStretch()

        h_box = QHBoxLayout()
        h_box.addStretch()
        # h_box.addWidget(self.input_frame)
        # h_box.addStretch()
        h_box.addLayout(v_box)
        h_box.addStretch()
        self.setLayout(h_box)

    def get_photo_path(self):
        self.photo_path = QFileDialog.getExistingDirectory(self, "Выберите папку с исходниками",
                                                           os.getenv("HOME"))  # 'C://'
        if self.photo_path != "":
            self.input_photo_path.setText(self.photo_path.split("/")[-1])

    def add_photo_logo(self):

        if (self.photo_path != ""
                and self.logo_path != ""):

            for file in os.listdir(self.photo_path):
                if file.lower().endswith('.jpg'):
                    if not os.path.isdir(f'{self.photo_path}/mix'):
                        os.mkdir(f'{self.photo_path}/mix')
                    base_image = Image.open(f'{self.photo_path}/{file}')
                    logo = Image.open(self.logo_path)
                    width, height = base_image.size

                    transparent = Image.new('RGB', (width, height), (0, 0, 0, 0))
                    transparent.paste(base_image, (0, 0))

                    fixed_width = int(base_image.width / 100 * 15)
                    width_percent = fixed_width / logo.width * 100
                    height_size = int(logo.height / 100 * width_percent)
                    logo_resize = logo.resize((fixed_width, height_size))
                    indent = int(base_image.height / 100 * 5)
                    position = (base_image.width - (logo_resize.width + indent),
                                base_image.height - (logo_resize.height + indent))
                    transparent.paste(logo_resize, position, mask=logo_resize)
                    # transparent.show()
                    transparent.save(f'{self.photo_path}/mix/SiriusAutodrom({file.split(".")[0]}).jpg')
            self.input_start.setEnabled(False)

        else:
            QMessageBox.about(self, "Info", "Не выбрана папка фото!")

        os.startfile(f'{self.photo_path}/mix')
        sys.exit(app.exec_())


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.window = LogoMixer()
        self.setCentralWidget(self.window)
        self.setWindowTitle("Лого-миксер")
        self.show()


app = QApplication(sys.argv)
app.setStyle("Fusion")


def create_palette():
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(50, 50, 50))
    palette.setColor(QPalette.WindowText, Qt.gray)
    palette.setColor(QPalette.Base, QColor(30, 30, 30))
    palette.setColor(QPalette.AlternateBase, QColor(50, 50, 50))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(50, 50, 50))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(40, 130, 220))
    palette.setColor(QPalette.Highlight, QColor(40, 130, 220))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    return palette


app.setPalette(create_palette())
main_window = MainWindow()
sys.exit(app.exec_())
