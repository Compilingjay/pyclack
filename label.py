from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel


class SettingLabel(QLabel):

    def __init_subclass__(
            cls,
            text: str,
            align_flag: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignCenter) -> None:
        super().__init_subclass__()

        cls.setAlignment(cls, align_flag)
        cls.setText(text)
        return cls