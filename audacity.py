import sys
import os

class Audacity:
    def __init__(self):
        if sys.platform == 'win32':
            TONAME = '\\\\.\\pipe\\ToSrvPipe'
            FROMNAME = '\\\\.\\pipe\\FromSrvPipe'
            self._EOL = '\r\n\0'
        else:
            TONAME = '/tmp/audacity_script_pipe.to.' + str(os.getuid())
            FROMNAME = '/tmp/audacity_script_pipe.from.' + str(os.getuid())
            self._EOL = '\n'
        self._TOFILE = open(TONAME, 'w')
        self._FROMFILE = open(FROMNAME, 'rt')

    def send_command(self, command):
        self._TOFILE.write(command + self._EOL)
        self._TOFILE.flush()

    def get_response(self):
        result = ''
        line = ''
        while True:
            result += line
            line = self._FROMFILE.readline()
            if line == '\n' and len(result) > 0:
                break
        return result

    def do_command(self, command):
        self.send_command(command)
        response = self.get_response()
        return response

class AudacityControl:
    def __init__(self, audacity, verbose=False):
        self._audacity = audacity
        self._verbose = verbose

    def _do_command(self, command):
        if self._verbose:
            print(command)
            result = self._audacity.do_command(command)
            print(result)
        else:
            self._audacity.do_command(command)

    def new_mono_track(self):
        self._do_command('NewMonoTrack:')

    def export_as_wave(self, file_name_str, num_channels):
        self._do_command('Export2: Filename="' + file_name_str + '" ' + 'NumChannels="' + str(num_channels) + '"')

    def select_all(self):
        self._do_command('SelectAll:')

    def select_from_top(self, start_time, end_time):
        self._do_command('Select: End="' + str(end_time) +'" ' + 'Mode="Set" ' + 'Start="' + str(start_time) + '"')

    def truncate_silence(self):
        self._do_command('TruncateSilence:Action="Truncate Detected Silence" Compress="50" Independent="0" Minimum="2" Threshold="-80" Truncate="0.5"')

    def normalize(self):
        self._do_command('Normalize: ApplyGain="1" PeakLevel="0" RemoveDcOffset="0" StereoIndependent="0"')

    def delete_track(self):
        self._do_command('TrackClose:')

    def start_record(self):
        self._do_command('Record1stChoice:')

    def stop(self):
        self._do_command('Stop:')

    def save_as_project(self, file_name_str):
        self._do_command('SaveProject2:AddToHistory="0" Filename="' + file_name_str + '"')

if __name__ == "__main__":
    audacity_control = AudacityControl(Audacity())
    audacity_control.new_mono_track()
