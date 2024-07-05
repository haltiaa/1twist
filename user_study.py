import json
import time
import msvcrt

from classes import Dataset


def get_user_response():
    print("Press the left arrow key for YES and the right arrow key for NO.")
    while True:
        key = msvcrt.getch()
        if key == b'\xe0':  # Arrow keys are two bytes in Windows: '\xe0' followed by the key code
            key = msvcrt.getch()
            if key == b'K':  # Left arrow key code
                return 'yes'
            elif key == b'M':  # Right arrow key code
                return 'no'

def save_responses(responses, filename):
    with open(filename, 'w') as file:
        json.dump(responses, file, indent=4)


def main(instructions):
    dataset = Dataset()
    user_responses = []

    for problem in dataset:
        choiceA, choiceB = problem["A"], problem["B"]

        print(instructions)
        print(f"A: {choiceA}\t\tB: {choiceB}")

        start_time = time.time()
        response = get_user_response()
        end_time = time.time()
        time_taken = end_time - start_time
        responses.append({'question': question, 'response': response, 'time_taken': time_taken})

    save_responses(responses, 'responses.json')

if __name__ == "__main__":
    main()
