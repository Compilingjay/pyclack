from PySide6.QtCore import Slot, Signal, QRunnable, QObject
from typing import Callable


class WorkerSignals(QObject):
    finish = Signal()
    error = Signal()


class Worker(QRunnable):

    def __init__(self, func: Callable[[], None], *args: tuple) -> None:
        super().__init__()
        self._func: Callable[[], None] = func
        self._args = args
        self._signals = WorkerSignals()


    @Slot()
    def run(self) -> None:
        try:
            self._func(*self._args)
        finally:
            self._signals.finish.emit()