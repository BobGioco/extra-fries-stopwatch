import os
import argparse
import time
import simpleaudio as sa
from art import tprint

parser = argparse.ArgumentParser(description='Process some integers.')

parser.add_argument('-r', '--rounds', help='Number of rounds', type=int)
parser.add_argument('-e', '--exercises', help='Number of exercises', type=int)
parser.add_argument('-d', '--duration', help='Duration of one exercise', type=int)

parser.add_argument('-eb', '--exercise_break', help='Duration of one exercise', type=int)
parser.add_argument('-rb', '--round_break', help='Duration of one exercise', type=int)

args = parser.parse_args()

sound_files = (
   ('short_whistle', './sounds/whistle_short.wav'),
   ('long_whistle', './sounds/whistle_long.wav'),
   ('buzzer', './sounds/buzzer.wav'),
   ('beep', './sounds/beep.wav'),
)

def build_sounds(files: tuple) -> dict:
    """
    Create and return a dictionary of simpleaudio.WaveObject instances from a tuple of file descriptors.

    The function iterates over a tuple of file descriptors, each being a tuple with a label and a file path.
    It loads each audio file as a WaveObject and stores it in a dictionary with its corresponding label as the key.

    Args:
    files (tuple): A tuple of tuples, where each inner tuple contains a label (str) and a file path (str)
                   to a WAV file, e.g., (('label1', 'path/to/file1.wav'), ('label2', 'path/to/file2.wav'))

    Returns:
    dict: A dictionary where each key is a label (str) from the input tuple and each value is the corresponding
          WaveObject created from the WAV file at the given file path.

    """
    output = dict()
    for file in sound_files:
        print(file)
        output[file[0]] = sa.WaveObject.from_wave_file(file[1])
    return output

def clear_screen() -> None:
    """
    Clear CLI screen
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def display(round: int, rounds_total: int, exercise: int, exercise_total: int, time_counter: int, break_name=None, break_time=None) -> None:
    """
    Clears the screen and displays the current status of a workout session including round, exercise, and time information.

    This function is responsible for the real-time visual representation of the workout progress. It shows the current round and exercise numbers out of the total, along with a countdown timer. Optionally, it can also display break information.

    Args:
    round (int): The current round number.
    rounds_total (int): The total number of rounds in the workout session.
    exercise (int): The current exercise number within the current round.
    exercise_total (int): The total number of exercises within each round.
    time_counter (int): A countdown timer value (in seconds).
    break_name (str, optional): The name of the current break, if applicable. Defaults to None.
    break_time (int, optional): The duration of the current break (in seconds), if applicable. Defaults to None.

    Returns:
    None: This function does not return anything. It outputs directly to the console.
    """
    clear_screen()
    print(f"Round: {round}/{rounds_total}")
    print(f"Exercise: {exercise}/{exercise_total}")
    tprint(f"{time_counter:02d}", 'standard')
    if break_name:
        print(f"{break_name} break: {break_time:02d}")

def apply_break(round: int, rounds:int, exercise: int, exercises: int, break_name: str, break_time: int) -> None:
    """
    Manages and displays the break period between exercises or rounds during a workout session.

    This function counts down the break time, updating the display every second. It shows the remaining time of the break, along with a label indicating whether it's an exercise break or a round break.

    Args:
    round (int): The current round number.
    rounds (int): The total number of rounds in the workout session.
    exercise (int): The number of the next exercise after the break, or 0 if the break is between rounds.
    exercises (int): The total number of exercises in each round.
    break_name (str): A label indicating the type of break ('Exercise' or 'Round').
    break_time (int): The duration of the break in seconds.

    Returns:
    None: This function does not return anything. It performs a countdown and updates the display in real-time.
    """
    for second in range(0, break_time + 1):
        display(round, rounds, exercise, exercises, 0, break_name,break_time-second)
        time.sleep(1)

def start(sound: sa.shiny.WaveObject) -> None:
    """
    Executes a countdown from 10 seconds to 0, updating the display every second, and plays a sound when close to zero.

    This function is used to give a preparatory countdown before the start of the workout session. It clears the screen, displays the countdown timer, and plays a given sound for the last 4 seconds of the countdown.

    Args:
    sound (sa.shiny.WaveObject): A WaveObject from the simpleaudio module, which will be played during the final 4 seconds of the countdown.

    Returns:
    None: This function does not return anything. It outputs the countdown timer to the console and plays a sound.
    """
    for i in range(-10, 0):
        clear_screen()
        print("We start in")
        tprint(f"{(-i):02d}", 'standard')
        if i > -4:
            sound.play()
        time.sleep(1)

def main() -> None:
    rounds = args.rounds
    exercises = args.exercises
    duration = args.duration
    exercise_break = int(args.exercise_break) if args.exercise_break else 15
    round_break = int(args.round_break) if args.round_break else 60
    sounds = build_sounds(sound_files)

    start(sounds['beep'])
    for round in range(1, rounds+1):
        for exercise in range(1, exercises+1):
            sounds['short_whistle'].play()
            for time_counter in range(0, duration + 1):
                diff = duration-time_counter
                display(round, rounds, exercise, exercises, diff)
                if diff <= 3:
                    sounds['beep'].play()
                time.sleep(1)
            if exercise != exercises:
                sounds['long_whistle'].play()
                apply_break(round, rounds, exercise + 1, exercises, 'Exercise', exercise_break)

        sounds['buzzer'].play()
        if round != rounds:
            apply_break(round + 1, rounds, 0, exercises, 'Round', round_break)
    print('Extra fries are done for today!')

if __name__ == "__main__":
    main()