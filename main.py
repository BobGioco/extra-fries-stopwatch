import os
import argparse
import time

parser = argparse.ArgumentParser(description='Process some integers.')

parser.add_argument('-r', '--rounds', help='Number of rounds')
parser.add_argument('-e', '--exercises', help='Number of exercises')
parser.add_argument('-d', '--duration', help='Duration of one exercise')

parser.add_argument('-eb', '--exercise_break', help='Duration of one exercise')
parser.add_argument('-rb', '--round_break', help='Duration of one exercise')

args = parser.parse_args()

def clear_screen():
    # Clear the command line screen.
    os.system('cls' if os.name == 'nt' else 'clear')

def validate_number(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return None

def display(round, exercise, exercise_total, time_counter, break_name=None, break_time=None):

    clear_screen()
    print(f"Round: {round}")
    print(f"Exercise: {exercise}/{exercise_total}")
    print(f"{time_counter:02d}")
    if break_name:
        print(f"{break_name} break: {break_time:02d}")

def apply_break(round, exercise, exercises, break_name, break_time):
    for second in range(0, break_time + 1):
        display(round, exercise, exercises, 0, break_name, second)
        time.sleep(1)
        

def main():
    rounds = int(args.rounds)
    exercises = int(args.exercises)
    duration = int(args.duration)
    exercise_break = int(args.exercise_break) if args.exercise_break else 15
    round_break = int(args.round_break) if args.round_break else 60

    print(f"round: {rounds}\nexercises: {exercises}\nduration: {duration}")

    for round in range(1, rounds+1):
        for exercise in range(1, exercises+1):
            for time_counter in range(0, duration + 1):
                display(round, exercise, exercises, time_counter)
                time.sleep(1)
            if exercise != exercises:
                apply_break(round, exercise + 1, exercises, 'Exercise', exercise_break)
        time.sleep(29)
        if round != rounds:
            apply_break(round + 1, 0, exercises, 'Round', exercise_break)
    print('Extra fries are done for today!')

if __name__ == "__main__":
    main()