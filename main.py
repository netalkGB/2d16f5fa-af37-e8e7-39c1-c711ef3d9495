import sys
import os
import json
import subprocess
import time
from audacity import Audacity, AudacityControl
import pretty_midi

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
    midi_abspath = os.path.abspath(midi_path)
    midi_data = pretty_midi.PrettyMIDI(midi_path)

    duration_seconds = midi_data.get_end_time()
    margin_rec_seconds = int(config['marginRecSeconds']) # Add extra startup time for the player and cut silence to get by.
    rec_time_seconds = duration_seconds + margin_rec_seconds
    
    audacity.start_record()
    print('Start recording.')
    process = subprocess.Popen(config['midiPlayerPath'] + ' ' + midi_abspath)
    print('Start midi player process.')

    time.sleep(rec_time_seconds) # approximately
    
    audacity.stop() 
    print('Stop recording.')
    process.kill()
    print('Kill midi player process.')

    midi_file_name = os.path.basename(midi_abspath)
    project_file_path = os.path.join(config['projectFileOutPath'], midi_file_name + '.aup3')
    audacity.save_as_project(project_file_path)
    print('Save as project file before processing. => ' + project_file_path)

    audacity.select_from_top(0, 10)
    audacity.truncate_silence()
    print('Remove silence at start.')
    
    audacity.select_all()
    audacity.normalize()
    print('Normalize.')

    audacity.select_all()
    wave_file_path = os.path.join(config['waveFileOutPath'], midi_file_name + '.wav')
    audacity.export_as_wave(wave_file_path, 2)
    print('Export as wave file. => ' + wave_file_path)

    audacity.select_all()
    audacity.delete_track()

    print('[end] ' + str(idx + 1) + '/' + str(file_count) + ' ' + midi_path)
    
    time.sleep(3)
