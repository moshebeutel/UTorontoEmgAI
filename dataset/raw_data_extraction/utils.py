from collections.abc import Callable
from functools import partial
from pathlib import Path
import config
from load_rhd_notebook_python.importrhdutilities import load_file


def get_participant_root(participant_num: int) -> Path:
    participants_root = config.get('PARTICIPANTS_ROOT')
    participants_path = Path(participants_root)
    assert participants_path.exists(), f'Participants directory does not exist: {participants_path}'
    assert participants_path.is_dir(), f'Participants directory is not a directory: {participants_path}'
    participant_path = participants_path / f'Participant {participant_num}'
    assert participant_path.exists(), f'Participant directory does not exist: {participant_path}'
    assert participant_path.is_dir(), f'Participant directory is not a directory: {participant_path}'
    return participant_path


def get_rhd_gen_in_gesture_folder(gesture_path: Path):
    assert gesture_path.is_dir(), f'Expected a gesture folder. Got {gesture_path.as_posix()}'
    print(gesture_path)
    print(type(gesture_path))
    l_gesture_paths = list(gesture_path.iterdir())
    for record_folder in l_gesture_paths:
        rhd_path: Path = next(iter(record_folder.glob('*.rhd')))
        assert rhd_path.exists()
        yield rhd_path


def get_gestures_gen(test_path: Path, phase_name: str = 'Test Data (Keys)'):
    assert test_path.is_dir(), f'Expected test folder. Got {test_path}'
    phase_folder = test_path / phase_name
    assert phase_folder.is_dir(), f'Expected  phase folder. Got {phase_folder}'
    gestures_paths_gen = phase_folder.iterdir()
    return gestures_paths_gen


def get_phase_data_dict(test_path: Path, phase_name: str = 'Test Data (Keys)') -> dict[str, Callable]:
    gestures_paths_gen = get_gestures_gen(test_path, phase_name)
    return {gp.name: partial(get_rhd_gen_in_gesture_folder, gp) for gp in gestures_paths_gen}


def get_amplifier_data(participant_num: int, test_num: int, phase_name: str, gesture_name: str):
    assert participant_num in range(1, 21), f'Expected participant num between 1-20. Got {participant_num}'
    assert test_num in [1, 2], f'Expected test num be 1 or 2. Got {test_num}'
    assert phase_name in ['Preliminary Testing Movements', 'Test Data (Keys)',
                          'Test Data (Sentence)'], (f'Expected phase name be one of [Preliminary Testing Movements,'
                                                    f'Test Data (Keys),Test Data (Sentence)]. Got {phase_name}')

    participant_path: Path = get_participant_root(participant_num)
    test_path = participant_path / f'Test {test_num}'
    record_data_dict: dict[str, Callable] = get_phase_data_dict(test_path, phase_name=phase_name)
    print(record_data_dict.keys())
    assert gesture_name in record_data_dict, f'Expected one of {record_data_dict.keys()}. Got {gesture_name}'
    rhd_path_gen = record_data_dict[gesture_name]()
    print(rhd_path_gen)
    rhd_path = next(iter(rhd_path_gen))
    assert rhd_path.exists(), f'Expected path to rhd file. Got not existing path {rhd_path.as_posix()}'
    assert rhd_path.suffix == '.rhd', f'Expected path to rhd file. Got {rhd_path.name}'
    print('Loading ', rhd_path.as_posix())
    data, data_present = load_file(rhd_path.as_posix())
    assert data_present, f'data not present for {gesture_name}'
    print('Data loaded, keys:', data.keys())
    return data['t_amplifier'], data['amplifier_data']


if __name__ == '__main__':
    participants_num = 10
    test_num = 2
    phase_name = 'Test Data (Keys)'
    gesture_name = 'g'
    timestamps, signal = get_amplifier_data(participants_num, test_num, phase_name, gesture_name)
    print(timestamps.shape, signal.shape)
