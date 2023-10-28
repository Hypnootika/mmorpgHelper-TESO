from win32gui import FindWindow, SetForegroundWindow, SetWindowPos
from win32con import HWND_TOP, SWP_NOSIZE


WINDOW_SUBSTRING = "Elder Scrolls Online"


class ProcessHelper:
    def __init__(self, hwnd=None) -> None:
        self.hwnd = self.get_hwnd(hwnd)

    def get_hwnd(self, hwnd=None):
        if hwnd is None:
            hwnd = self.find_window()
            if hwnd == 0:
                raise Exception(WINDOW_SUBSTRING + " window not found", hwnd)
        else:
            hwnd = hwnd

        return hwnd

    @staticmethod
    def find_window(classname=None):
        hwnd = FindWindow(classname, WINDOW_SUBSTRING)
        return hwnd

    def set_foreground_window(self):
        SetForegroundWindow(self.hwnd)

    def set_window_pos(self, x=0, y=0, flag=HWND_TOP):
        """specify that the window is displayed at the top, etc., see: win32api SetWindowPos"""
        SetWindowPos(self.hwnd, flag, x, y, 0, 0, SWP_NOSIZE)
