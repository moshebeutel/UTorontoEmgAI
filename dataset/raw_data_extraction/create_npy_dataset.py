from functools import partial
import numpy as np
from experiment import test_numbers, experiment_phases, phases_gestures, participant_numbers_range
from dataset.raw_data_extraction.utils import get_amplifier_data


def save_participant_test_phase_gesture_to_npy(get_amplifier_data_fn, gesture_name, file_prefix):
    timestamps, signal = get_amplifier_data_fn(gesture_name)
    file_prefix += f'_gesture_{gesture_name}'
    with open(f'{file_prefix}.npy', 'wb') as f:
        np.save(f, timestamps)
        np.save(f, signal)


def save_participant_test_phase_to_npy(get_amplifier_data_fn, phase_name, file_prefix):
    get_amplifier_data_fn = partial(get_amplifier_data_fn, phase_name)
    file_prefix += f'_phase_{phase_name}'
    for gesture_name in phases_gestures[phase_name]:
        save_participant_test_phase_gesture_to_npy(get_amplifier_data_fn, gesture_name, file_prefix)


def save_participant_test_to_npy(get_amplifier_data_fn, test_num, file_prefix):
    get_amplifier_data_fn = partial(get_amplifier_data_fn, test_num)
    file_prefix += f'_test_{test_num}'
    for phase_name in experiment_phases:
        save_participant_test_phase_to_npy(get_amplifier_data_fn, phase_name, file_prefix)


def save_participant_data_to_npy(participant_num: int):
    get_amplifier_data_fn = partial(get_amplifier_data, participant_num)
    file_prefix = f'participant_{participant_num}'
    for test_num in test_numbers:
        save_participant_test_to_npy(get_amplifier_data_fn, test_num, file_prefix)


def save_all_participants_data():
    for participant_num in participant_numbers_range:
        save_participant_data_to_npy(participant_num)


if __name__ == '__main__':
    save_all_participants_data()
