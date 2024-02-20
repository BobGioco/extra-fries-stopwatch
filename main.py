import os
import argparse
import time
import simpleaudio as sa
from art import tprint

parser = argparse.ArgumentParser(description='Process some integers.')

parser.add_argument('-r', '--rounds', help='Number of rounds')
parser.add_argument('-e', '--exercises', help='Number of exercises')
parser.add_argument('-d', '--duration', help='Duration of one exercise')

parser.add_argument('-eb', '--exercise_break', help='Duration of one exercise')
parser.add_argument('-rb', '--round_break', help='Duration of one exercise')

args = parser.parse_args()

sound_files = (
   ('short_whistle', './sounds/whistle_short.wav'),
   ('long_whistle', './sounds/whistle_long.wav'),
   ('buzzer', './sounds/buzzer.wav'),
)

def build_sounds(files: tuple) -> dict:
    output = dict()
    for file in sound_files:
        print(file)
        output[file[0]] = sa.WaveObject.from_wave_file(file[1])
    return output

def clear_screen():
    # Clear the command line screen.
    os.system('cls' if os.name == 'nt' else 'clear')

def validate_number(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return None

def display(round, rounds_total, exercise, exercise_total, time_counter, break_name=None, break_time=None):

    clear_screen()
    print(f"Round: {round}/{rounds_total}")
    print(f"Exercise: {exercise}/{exercise_total}")
    tprint(f"{time_counter:02d}", 'standard')
    if break_name:
        print(f"{break_name} break: {break_time:02d}")

def apply_break(round: int, rounds:int, exercise: int, exercises: int, break_name: str, break_time: int):
    for second in range(0, break_time + 1):
        display(round, rounds, exercise, exercises, 0, break_name,break_time-second)
        time.sleep(1)
        

def main():
    rounds = int(args.rounds)
    exercises = int(args.exercises)
    duration = int(args.duration)
    exercise_break = int(args.exercise_break) if args.exercise_break else 15
    round_break = int(args.round_break) if args.round_break else 60
    sounds = build_sounds(sound_files)
    print(sounds)
    print(f"round: {rounds}\nexercises: {exercises}\nduration: {duration}")

    for round in range(1, rounds+1):
        for exercise in range(1, exercises+1):
            sounds['short_whistle'].play()
            for time_counter in range(0, duration + 1):
                display(round, rounds, exercise, exercises, duration-time_counter)
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