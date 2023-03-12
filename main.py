import sys
import os
import json
import time
from audacity import Audacity, AudacityControl
from player import Player

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
player = Player(config['midiPlayerPath'], config['playingWindowTitle'])

for idx, midi_path in enumerate(playlist):
    print('[start] ' + str(idx + 1) + '/' + str(file_count) + ' ' + midi_path)

    player.play(os.path.abspath(config['resetMidiFilePath']))
    
    midi_abspath = os.path.abspath(midi_path)
    print('Start recording.')
    audacity.start_record()
    player.play(midi_abspath)

    time.sleep(int(config['marginRecSeconds']))

    print('Stop recording.')
    audacity.stop() 

    print('Normalize.')
    audacity.select_all()
    audacity.normalize()

    midi_file_name = os.path.basename(midi_abspath)

    wave_file_path = os.path.join(config['waveFileOutPath'], midi_file_name + '.wav')
    print('Export as wave file. => ' + wave_file_path)
    audacity.select_all()
    audacity.export_as_wave(wave_file_path, 2)
    

    project_file_path = os.path.join(config['projectFileOutPath'], midi_file_name + '.aup3')
    print('Save as project file. => ' + project_file_path)
    audacity.save_as_project(project_file_path)

    audacity.close()

    print('[end] ' + str(idx + 1) + '/' + str(file_count) + ' ' + midi_path)
