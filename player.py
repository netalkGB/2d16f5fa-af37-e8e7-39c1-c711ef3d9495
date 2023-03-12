import windows
import time
import subprocess

class Player:
    def __init__(self, player_path, playing_window_title, window_title_poll_interval_seconds=0.1):
        self._player_path = player_path
        self._playing_window_title = playing_window_title
        self._window_title_poll_interval_seconds = window_title_poll_interval_seconds

    def _is_playing_midi(self):
        window_titles = windows.get_window_titles()
        return len([title for title in window_titles if title.find(self._playing_window_title) >= 0]) > 0

    def _wait_for_playback(self):
        while True:
            if self._is_playing_midi() == True:
                break
            time.sleep(self._window_title_poll_interval_seconds)

    def _wait_for_stop(self):
        while True:
            if self._is_playing_midi() == False:
                break
            time.sleep(self._window_title_poll_interval_seconds)

    def play(self, file_path):
        subprocess.Popen(self._player_path + ' ' + file_path)
        self._wait_for_playback()
        self._wait_for_stop()
