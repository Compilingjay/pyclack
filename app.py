from PySide6 import QtWidgets
from PySide6.QtCore import Slot, QKeyCombination, Qt, QThreadPool
from PySide6.QtGui import QCloseEvent, QKeySequence, QWindow
from PySide6.QtWidgets import QDialog, QDoubleSpinBox, QGridLayout, QGroupBox, QKeySequenceEdit

import time, keyboard, mouse
from functools import partial
from typing import Callable

import settings
from worker import Worker
from label import SettingLabel
from map_keys import qtToKeyboardLibraryKeys
    

class PyClackApp(QDialog):

    def __init__(self) -> None:
        super().__init__()
        self._autoclick_on = False
        self._index_edit_widget = 0
        self._num_edit_widgets = 3
        self.thread_pool = QThreadPool()

        self.setWindowTitle("PyClicker")

        settings.init()
        _success = settings.loadConfig()

        click_start_label = SettingLabel("Start Autoclicker")
        click_start_edit: tuple[QKeySequenceEdit] = [QKeySequenceEdit()]
        click_start_setting: str = "[DEFAULT]\nkey_click"
        click_start_edit[0].setMaximumSequenceLength(1)
        click_start_edit[0].setFocusPolicy(Qt.FocusPolicy.TabFocus)
        click_start_edit[0].editingFinished.connect(
            partial(self.updateKeyEditSequence,
                    click_start_edit,
                    click_start_setting,
                    self.startClick))

        click_stop_label = SettingLabel("Stop Autoclicker")
        click_stop_edit: tuple[QKeySequenceEdit] = [QKeySequenceEdit()]
        click_stop_setting: str = "[DEFAULT]\nkey_stop"
        click_stop_edit[0].setMaximumSequenceLength(1)
        click_stop_edit[0].setFocusPolicy(Qt.FocusPolicy.TabFocus)
        click_stop_edit[0].editingFinished.connect(
            partial(self.updateKeyEditSequence,
                    click_stop_edit,
                    click_stop_setting,
                    self.stopClick))
        
        click_per_sec_label = SettingLabel("Clicks Per Second (0.1-500)")
        clicks_per_sec_edit: tuple[QKeySequenceEdit] = [QDoubleSpinBox()]
        clicks_per_sec_setting: str = "[DEFAULT]\nclicks_per_second"
        clicks_per_sec_edit[0].setDecimals(1)
        clicks_per_sec_edit[0].setMinimum(0.1)
        clicks_per_sec_edit[0].setMaximum(500.0)
        clicks_per_sec_edit[0].setFocusPolicy(Qt.FocusPolicy.TabFocus)
        clicks_per_sec_edit[0].editingFinished.connect(
            partial(self.updateSpinBox,
                    clicks_per_sec_edit,
                    clicks_per_sec_setting,
                    self.updateClicksPerSecond))
        clicks_per_sec_edit[0].valueChanged.connect(
            partial(self.updateSpinBox,
                    clicks_per_sec_edit,
                    clicks_per_sec_setting,
                    self.updateClicksPerSecond))
        
        app_layout = QGridLayout(self)
        settings_groupbox = QGroupBox("Settings")
        settings_layout = QGridLayout(settings_groupbox)

        settings_layout.addWidget(click_start_label, 0, 0)
        settings_layout.addWidget(click_stop_label, 1, 0)
        settings_layout.addWidget(click_per_sec_label, 2, 0)

        settings_layout.addWidget(click_start_edit[0], 0, 1)
        settings_layout.addWidget(click_stop_edit[0], 1, 1)
        settings_layout.addWidget(clicks_per_sec_edit[0], 2, 1)

        settings_layout.setContentsMargins(12, 0, 12, 6)
        app_layout.addWidget(settings_groupbox)
        self.setLayout(app_layout)

        click_start_edit_keys = settings.config["DEFAULT"]["key_click"]
        click_start_edit[0].setKeySequence(click_start_edit_keys)
        keyboard.add_hotkey(click_start_edit_keys, self.startClick)
        
        click_stop_edit_keys = settings.config["DEFAULT"]["key_stop"]
        click_stop_edit[0].setKeySequence(click_stop_edit_keys)
        keyboard.add_hotkey(click_stop_edit_keys, self.stopClick)

        clicks_per_second = float(settings.config["DEFAULT"]["clicks_per_second"])
        clicks_per_sec_edit[0].setValue(clicks_per_second)

        # self.setFocus()


    def startClick(self) -> None:
        if self._autoclick_on:
            return
        click_worker = Worker(self.click)
        self.thread_pool.start(click_worker)


    def stopClick(self) -> None:
        self._autoclick_on = False
    

    def click(self) -> None:
        delay = 1.0 / float(settings.config["DEFAULT"]["clicks_per_second"])
        self._autoclick_on = True
        clicks = 0
        start = time.monotonic()
        current_time = time.monotonic()
        while self._autoclick_on:
            if time.monotonic() - current_time > 0:
                mouse.click()
                current_time += delay
                clicks += 1
        
        # log: print(time.monotonic() - start, ", ", clicks)


    def closeEvent(self, _event: QCloseEvent) -> None:
        self.stopClick()
        _success = settings.saveConfig()
        self.thread_pool.clear()
    

    def rebindHotkey(self, new_keys: str, old_keys: str, hotkey_func: Callable) -> None:
        keyboard.remove_hotkey(old_keys)
        keyboard.add_hotkey(new_keys, hotkey_func)
    

    def updateClicksPerSecond(self, widget: tuple[QDoubleSpinBox], setting_path: str) -> None:
        setting: list[str] = setting_path.split('\n')
        assert len(setting) < 3

        clicks_per_second: float = widget[0].value()
        settings.config["DEFAULT"]["clicks_per_second"] = str(clicks_per_second)


    @Slot()
    def updateKeyEditSequence(self, key_edit: tuple[QKeySequenceEdit], setting_path: str, hotkey_func: Callable) -> None:
        self.trackFocus()
        self._autoclick_on = False
        key_widget: QKeySequenceEdit = key_edit[0]

        setting: list[str] = setting_path.split('\n')
        assert len(setting) < 3

        prev_keys: QKeySequence = settings.config.get(section=setting[0][1:-1], option=setting[1])
        key_combination: QKeyCombination = None
        try:
            key_combination = key_widget.keySequence()[0]
        except:
            # log key error
            key_edit[0].setKeySequence(prev_keys)
            return

        new_keys: str = ""
        modifiers: Qt.KeyboardModifier = key_combination.keyboardModifiers()
        if modifiers is not Qt.KeyboardModifier.NoModifier:
            for mod in modifiers:
                m: Qt.Key = None
                match mod:
                    case Qt.KeyboardModifier.ShiftModifier:
                        m = Qt.Key.Key_Shift
                    case Qt.KeyboardModifier.ControlModifier:
                        m = Qt.Key.Key_Control
                    case Qt.KeyboardModifier.AltModifier:
                        m = Qt.Key.Key_Alt
                    case _:
                        key_edit[0].setKeySequence(prev_keys)
                        return

                new_keys += qtToKeyboardLibraryKeys(m) + '+'
        
        k: Qt.Key = key_combination.key()
        new_keys += qtToKeyboardLibraryKeys(k)

        if settings.isKeyInConfig(new_keys, prev_keys):
            # log key already exists
            key_edit[0].setKeySequence(prev_keys)
            return
        
        settings.config.read_string(f"{setting_path}={new_keys}")
        key_edit[0].setKeySequence(new_keys)
        self.rebindHotkey(new_keys, prev_keys, hotkey_func)


    @Slot()
    def updateSpinBox(
            self,
            spin_box: tuple[QDoubleSpinBox],
            setting_path: str,
            update_func: Callable,
            _new_value: float = None) -> None:
        self.trackFocus()
        self._autoclick_on = False
        setting = setting_path.split('\n')
        assert len(setting) < 3

        prev_value: float = settings.config.getfloat(setting[0][1:-1], setting[1])

        curr_value = spin_box[0].value()
        if curr_value < spin_box[0].minimum() or curr_value > spin_box[0].maximum():
            # log error!
            spin_box[0].setValue(prev_value)
            return
        
        update_func(spin_box, setting_path)


    def trackFocus(self) -> None:
        self._index_edit_widget += 1
        if self._index_edit_widget >= self._num_edit_widgets:
            self.removeFocus()
            self._index_edit_widget = 0
    

    def removeFocus(self) -> None:
        focused_widget = QtWidgets.QApplication.focusWidget()
        if focused_widget is not None:
            focused_widget.clearFocus()
