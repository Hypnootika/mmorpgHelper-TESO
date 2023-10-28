from logging import Handler, Formatter
from PyQt5.QtCore import pyqtSignal, QObject


class Handler(QObject, Handler):
    new_record = pyqtSignal(object)

    def __init__(self, parent):
        super().__init__(parent)
        super(Handler).__init__()
        self.formatter = Formatter("[%(levelname)s] %(message)s")
        self.setFormatter(self.formatter)

    def emit(self, record):
        msg = self.format(record)
        # emit signal
        self.new_record.emit(msg)


class Formatter(Formatter):
    def formatException(self, ei):
        return super().formatException(ei)

    def format(self, record):
        s = super().format(record)
        if record.exc_text:
            s = s.replace("\n", "")
        return s
