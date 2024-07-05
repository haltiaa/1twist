import sys
import termios
import threading
import time
import tty
import uuid
import select

import numpy as np
import pandas as pd

from classes import Dataset


def get_user_response(time=None):
    print("Press the left arrow key for A, the right arrow key for B")
    if time is not None:
        print(f"You only have {time}s to answer.")

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    response = {'answered': False, 'response': 'no answer'}

    def timer():
        nonlocal response
        time.sleep(time)
        if not response['answered']:
            response['answered'] = True

    if time is not None:
        timer_thread = threading.Thread(target=timer)
        timer_thread.start()

    try:
        tty.setraw(sys.stdin.fileno())
        while not response['answered']:
            if select.select([sys.stdin], [], [], 0.1)[0]:
                key = sys.stdin.read(3)
                if key == '\x1b[D':  # Left arrow key code
                    response = {'answered': True, 'response': 'A'}
                elif key == '\x1b[C':  # Right arrow key code
                    response = {'answered': True, 'response': 'B'}
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    return 0 if response['response'] == "A" else 1


def save_responses(responses, participant_id, session_id, mode):
    pd.DataFrame.from_records(responses).to_csv(f"{participant_id}_{mode}_{session_id}.csv")


def run_experiment(instructions, mode="long", ai_model=None, timing=5):
    assert mode in ["long", "short", "ai"], "Provided mode needs to be either long, short or ai"

    dataset = Dataset()
    user_responses = []

    participant_id = input("Please enter your participant ID: ")
    unique_session_id = str(uuid.uuid4())
    print(f"Thanks for joining {participant_id}. Your unique session ID: {unique_session_id}")
    print("-"*10)

    input("Are you ready to start? Press any key")

    if mode in ["short", "ai"] and (timing is None or timing <= 0):
        timing = 5
    else:
        timing = None

    for problem in dataset:
        choiceA, choiceB = problem["A"], problem["B"]

        print(instructions)
        print(f"A (left): {choiceA}\t\tvs.\t\tB (right): {choiceB}")

        # get the user's answer
        start_time = time.time()
        response = get_user_response()
        end_time = time.time(timing)
        time_first_response = end_time - start_time

        # provide the user with a recommendation, if ai model is provided
        if mode == "ai":
            recommendation = ai_model.evaluate_problem([choiceA, choiceB])

            print(f"They AI thinks that {'A' if recommendation == 0 else 'B'} is the right answer.")

            start_time = time.time()
            response = get_user_response(timing)
            end_time = time.time()
            after_ai_rec_timing = end_time - start_time
        else:
            after_ai_rec_timing = np.nan

        # no feedback prevented

        # store result
        user_responses.append({'problem_id': problem["Problem"],
                               'response': response,
                               'first_response_time': time_first_response,
                               'after_ai_time': after_ai_rec_timing})

    save_responses(user_responses, participant_id, unique_session_id)

    print("Thank you for participating!")


if __name__ == "__main__":
    run_experiment("Please decide", "long")
