import sys
import os
import json
import subprocess
import time
from audacity import Audacity, AudacityControl
import windows

if len(sys.argv) < 2:
    print('Error: Playlist must be specified.', file=sys.stderr)
    sys.exit(1)

playlist_path = sys.argv[1]

with open(os.path.join(os.getcwd(), 'config.json')) as f:
    config = json.load(f)   

with open(playlist_path) as f:
    playlist = f.read().splitlines()
    file_count = len(playlist)

print(str(file_count) + ' file(s)')

audacity = AudacityControl(Audacity(), config['verboseMode'])

for idx, midi_path in enumerate(playlist):
    print('[start] ' + str(idx + 1) + '/' + str(file_count) + ' ' + midi_path)

    subprocess.Popen(config['midiPlayerPath'] + ' ' + os.path.abspath(config['resetMidiFilePath']))
    print('Start midi player process.(reset)')
    while True:
        window_titles = windows.get_window_titles()
        is_playing = len([title for title in window_titles if title.find(config['playingWindowTitle']) >= 0]) > 0
        if is_playing == True:
            break
        time.sleep(0.1)    
    while True:
        window_titles = windows.get_window_titles()
        is_playing = len([title for title in window_titles if title.find(config['playingWindowTitle']) >= 0]) > 0
        if is_playing == False:
            break
        time.sleep(0.1)

    midi_abspath = os.path.abspath(midi_path)
    audacity.start_record()
    print('Start recording.')
    subprocess.Popen(config['midiPlayerPath'] + ' ' + midi_abspath)
    print('Start midi player process.')

    while True:
        window_titles = windows.get_window_titles()
        is_playing = len([title for title in window_titles if title.find(config['playingWindowTitle']) >= 0]) > 0
        if is_playing == True:
            break
        time.sleep(0.1)    
    while True:
        window_titles = windows.get_window_titles()
        is_playing = len([title for title in window_titles if title.find(config['playingWindowTitle']) >= 0]) > 0
        if is_playing == False:
            break
        time.sleep(0.1)
    
    time.sleep(int(config['marginRecSeconds']))

    audacity.stop() 
    print('Stop recording.')

    audacity.select_all()
    audacity.normalize()
    print('Normalize.')

    midi_file_name = os.path.basename(midi_abspath)

    audacity.select_all()
    wave_file_path = os.path.join(config['waveFileOutPath'], midi_file_name + '.wav')
    audacity.export_as_wave(wave_file_path, 2)
    print('Export as wave file. => ' + wave_file_path)

    project_file_path = os.path.join(config['projectFileOutPath'], midi_file_name + '.aup3')
    audacity.save_as_project(project_file_path)
    print('Save as project file. => ' + project_file_path)

    audacity.close()

    print('[end] ' + str(idx + 1) + '/' + str(file_count) + ' ' + midi_path)
    
    time.sleep(3)
