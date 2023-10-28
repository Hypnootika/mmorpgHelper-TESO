from logging import getLogger, info
from keyboard import add_hotkey
from threading import Thread, Lock
from time import sleep
from sys import exit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import (
    QApplication,
    QComboBox,
    QPlainTextEdit,
    QMainWindow,
    QGridLayout,
    QGroupBox,
    QPushButton,
    QHBoxLayout,
    QStyleFactory,
    QWidget,
)
from win32gui import SetForegroundWindow, FindWindow
from src.helper import config_helper, logging_helper, process_helper, name_helper
from src.engine import combat, toolbox
import asyncio
from random import uniform
import string
import random


class Overlay(QMainWindow):
    def __init__(self, parent=None):
        super(Overlay, self).__init__(parent)
        self.rotation_thread = None
        self.running = False
        self.pause = False
        self._lock = Lock()
        self.pause_req = False
        self.cfg = config_helper.read_config()
        self.name = name_helper.format_words(name_helper.get_word_pair())
        self.proc = process_helper.ProcessHelper()
        self.handler = None
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setWindowIcon(QIcon("..\\assets\\layout\\mmorpg_helper.ico"))
        QApplication.setStyle(QStyleFactory.create("Fusion"))
        self.setWindowTitle(self.name)
        self.setGeometry(1425, 850, 500, 170)
        self.setFixedSize(500, 170)
        visible_window = QWidget(self)
        visible_window.setFixedSize(500, 170)

        add_hotkey("end", lambda: self.on_press("exit"))
        add_hotkey("del", lambda: self.on_press("pause"))
        add_hotkey("capslock", lambda: self.on_press("pause"))

        self.createDropdownBox()
        self.createStartBox()
        self.createToolBox()
        self.createLoggerConsole()
        self.loggerConsole.setDisabled(False)
        self.invisible_stopbtn = QPushButton("STOP")
        self.invisible_stopbtn.clicked.connect(self.stop_record)
        mainLayout = QGridLayout()
        mainLayout.addWidget(self.invisible_stopbtn, 0, 0, 1, 3)
        mainLayout.addWidget(self.dropdownBox, 1, 0, 1, 1)
        mainLayout.addWidget(self.startBox, 1, 1, 1, 1)
        mainLayout.addWidget(self.toolBox, 1, 2, 1, 1)
        mainLayout.addWidget(self.loggerConsole, 2, 0, 2, 3)

        self.invisible_stopbtn.hide()
        mainLayout.setRowStretch(1, 1)
        mainLayout.setColumnStretch(1, 1)
        self.setCentralWidget(visible_window)
        visible_window.setLayout(mainLayout)
        self.rotation_thread = Thread(target=lambda: self.get_rotation())

    # prepare dropdownBox
    @staticmethod
    def update_class(item, value=None):
        info("Preset " + item + ": " + value)
        config_helper.save_config(item, value)

    def passCurrentText(self):
        self.update_class("class", self.ComboBox.currentText())

    def get_class(self):
        _ = []
        class_array = [
            "Dragonknight",
            "Nightblade Bow",
            "Nightblade Enrage",
            "Arcanist",
            "Necromancer",
            "Warden",
            "Sorcerer",
            "Templar",
        ]
        for class_var in class_array:
            result = QStandardItem(class_var)
            self.model.appendRow(result)
        self.ComboBox.setCurrentIndex(0)

    # loggerConsole
    def createLoggerConsole(self):
        if self.handler:
            getLogger().removeHandler(self.handler)
        self.loggerConsole = QWidget()
        layout = QHBoxLayout()

        self.handler = logging_helper.Handler(self)
        log_text_box = QPlainTextEdit(self)
        log_text_box.setStyleSheet(
            "background-color: rgba(255,255,255, 0); color: white"
        )
        log_text_box.setReadOnly(True)
        getLogger().addHandler(self.handler)
        # getLogger().setLevel(DEBUG)
        self.handler.new_record.connect(log_text_box.appendPlainText)

        layout.addWidget(log_text_box)
        self.loggerConsole.setLayout(layout)

    def closeEvent(self, event=None):
        if self.handler:
            getLogger().removeHandler(self.handler)
        self.destroy()
        QApplication.quit()

    def createDropdownBox(self):
        self.dropdownBox = QGroupBox()
        layout = QHBoxLayout()

        self.model = QStandardItemModel()
        self.ComboBox = QComboBox()
        self.ComboBox.setModel(self.model)

        self.get_class()
        self.ComboBox.activated.connect(self.passCurrentText)

        layout.addWidget(self.ComboBox)
        layout.addStretch(1)
        self.dropdownBox.setLayout(layout)

    # startBox
    def createStartBox(self):
        self.startBox = QGroupBox()
        layout = QHBoxLayout()

        toggleAssistButton = QPushButton("ASSISTANT")
        toggleAssistButton.setCheckable(True)
        toggleAssistButton.setChecked(False)
        toggleAssistButton.toggled.connect(self.toggle_rotation_thread)

        layout.addStretch(1)
        layout.addWidget(toggleAssistButton)
        layout.addStretch(1)
        self.startBox.setLayout(layout)

    # toolBox
    def createToolBox(self):
        self.toolBox = QGroupBox()
        layout = QHBoxLayout()

        toggleToolButton = QPushButton("TOOLBOX")
        toggleToolButton.setCheckable(False)
        toggleToolButton.setChecked(False)
        toggleToolButton.clicked.connect(self.littlehelper_toolbox)

        layout.addStretch(1)
        layout.addWidget(toggleToolButton)
        layout.addStretch(1)
        self.toolBox.setLayout(layout)

    def on_press(self, key):
        if key == "exit":
            info("_EXIT")

            if self.running:
                self.running = False
                self.rotation_thread.join()
            self.closeEvent()
        elif key == "pause":
            self.set_pause(not self.should_pause())
            if not self.pause:
                self.pause = True
                info("_PAUSE")
            else:
                self.pause = False
                info("_RUN")

    def should_pause(self):
        self._lock.acquire()
        pause_req = self.pause_req
        self._lock.release()
        return pause_req

    def set_pause(self, pause):
        self._lock.acquire()
        self.pause_req = pause
        self._lock.release()

    def toggle_rotation_thread(self, checked):
        if checked:
            self.get_rotation_thread()
        else:
            self.stop_rotation_thread()

    def get_rotation_thread(self):
        with self._lock:
            if self.rotation_thread is None or not self.rotation_thread.is_alive():
                self.rotation_thread = Thread(target=self.get_rotation)
                self.rotation_thread.start()

    def stop_rotation_thread(self):
        with self._lock:
            self.running = False
            if self.rotation_thread is not None:
                self.rotation_thread.join()
                self.rotation_thread = None

    def get_rotation(self):
        info("LittleHelper started")
        self.running = True

        while self.running:
            while self.should_pause():
                sleep(0.25)
            combat.rotation()
        info("LittleHelper stopped")

    def littlehelper_toolbox(self):
        if not hasattr(self, "app_toolbox"):
            self.app_toolbox = toolbox.Toolbox(self)
            self.app_toolbox.show()
            self.toolbox_created = True
        else:
            if self.app_toolbox.is_closed():
                self.app_toolbox = toolbox.Toolbox(self)
            self.app_toolbox.show()
            self.toolbox_created = True

    def start_record(self):
        self.invisible_stopbtn.show()
        self.app_toolbox.hide()

    def stop_record(self):
        self.app_toolbox.stop()
        self.app_toolbox.show()
