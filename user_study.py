import json
import time
import msvcrt
import uuid

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

    participant_id = input("Please enter your participant ID: ")
    unique_session_id = str(uuid.uuid4())
    print(f"Thanks for joining {participant_id}. Your unique session ID: {unique_session_id}")

    for problem in dataset:
        choiceA, choiceB = problem["A"], problem["B"]

        print(instructions)
        print(f"A: {choiceA}\t\tvs.\t\tB: {choiceB}")

        start_time = time.time()
        response = get_user_response()
        end_time = time.time()
        time_taken = end_time - start_time
        user_responses.append({'problem': problem["Problem"], 'response': response, 'time_taken': time_taken})

    save_responses(user_responses, 'responses_.json')


if __name__ == "__main__":
    main()
