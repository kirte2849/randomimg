import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtGui
from functools import partial
from ramdomimg import get_next_img, down_img
import os

import untitled

class ImgQue:
    def __init__(self):
        self.img_list = ['imgs/' + i for i in os.listdir('imgs/')]
        self.index = len(self.img_list) - 1

    def add(self, path):
        self.img_list.append(path)
        self.index = len(self.img_list) - 1

    def get_now(self):
        return self.img_list[self.index]

    def get_index(self):
        return self.index

    def next_one(self):
        self.index += 1
        self.index = self.index if self.index <= len(self.img_list) - 1 else len(self.img_list) - 1
        return self.img_list[self.index]

    def prev_one(self):
        self.index -= 1
        self.index = self.index if self.index >= 0 else 0
        return self.img_list[self.index]

    def show_local(self):
        return str(self.index)



img_manager = ImgQue()

def show_local(ui):
    try:
        s = img_manager.show_local()
        ui.local.setText(s)
    except Exception as e:
        print(f'at show local: {e}')


def new(ui):
    show_local(ui)
    this_page, img_url, discription = get_next_img()
    path = down_img(img_url)
    img_manager.add(path)
    print(f'at next path: {path}')
    ui.discription.setText(discription)
    jpg = QtGui.QPixmap(path)
    ui.label.setPixmap(jpg)

def next(ui):
    show_local(ui)
    jpg = QtGui.QPixmap(img_manager.next_one())
    ui.label.setPixmap(jpg)

def copy(ui):
    try:
        path = img_manager.get_now()
        with open(path, 'rb') as f:
            byte = f.read()
        with open(path.replace('imgs/', ''), 'wb') as f:
            f.write(byte)
    except Exception as e:
        print(e)

def prev(ui):
    show_local(ui)
    path = img_manager.prev_one()
    print(f'at prev path: {path}')
    jpg = QtGui.QPixmap(path)
    ui.label.setPixmap(jpg)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = untitled.Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()

    jpg = QtGui.QPixmap('imgs/start.jpg')
    ui.label.setPixmap(jpg)

    ui.next.clicked.connect(partial(next, ui))
    ui.new_2.clicked.connect(partial(new, ui))
    ui.prev.clicked.connect(partial(prev, ui))
    ui.copy.clicked.connect(partial(copy, ui))

    sys.exit(app.exec_())

