import ctypes

def get_window_titles():
    user32 = ctypes.windll.user32
    titles = []
    def foreach_window(hwnd, lparam):
        length = user32.GetWindowTextLengthW(hwnd)
        buf = ctypes.create_unicode_buffer(length + 1)
        user32.GetWindowTextW(hwnd, buf, length + 1)
        titles.append(buf.value)            
    user32.EnumWindows(ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))(foreach_window), 0)
    return titles

if __name__ == "__main__":
    print(get_window_titles())
