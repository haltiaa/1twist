import sys
import threading
import time
import uuid
import select

import numpy as np
import pandas as pd

from classes import Dataset


def get_user_response(time_limit=None):
    print("_"*50)
    print("Press the A key for A, press B key for B")
    if time is not None:
        print(f"You only have {time}s to answer.")

    def timer():
        t = 0
        while t < time_limit and not stop_flag.is_set():
            t += 1
            time.sleep(1)
            sys.stdout.write("\r" + f"{t} of {time_limit}s")
            sys.stdout.flush()

    stop_flag = threading.Event()
    timer_thread = threading.Thread(target=timer)
    timer_thread.start()

    a, b, c = select.select([sys.stdin], [], [], time_limit)
    stop_flag.set()
    timer_thread.join()

    # Run if statement till the time is running
    if (a):
        r = sys.stdin.readline().strip()
        print(f"Your answer: {r}")
        print("="*50)
        return 0 if r.lower() == "a" else "b"
    else:
        print("You failed to answer in time! Assuming reject.")
        print("="*50)
        return None


def save_responses(responses, participant_id, session_id, mode):
    pd.DataFrame.from_records(responses).to_csv(f"{participant_id}_{mode}_{session_id}.csv")


def run_experiment(instructions, mode="long", ai_model=None, timing=None):
    assert mode in ["long", "short", "ai"], "Provided mode needs to be either long, short or ai"

    dataset = Dataset()
    user_responses = []

    participant_id = input("Please enter your participant ID: ")
    unique_session_id = str(uuid.uuid4())
    print(f"Thanks for joining {participant_id}. Your unique session ID: {unique_session_id}")
    print("-"*10)

    input("Are you ready to start? Press enter to continue...")

    if mode in ["short", "ai"] and timing is None:
        timing = 10

    for problem in dataset:
        choiceA, choiceB = problem["A"], problem["B"]

        print(instructions)
        print(f"A (left): {choiceA}\t\tvs.\t\tB (right): {choiceB}")

        # get the user's answer
        start_time = time.time()
        response = get_user_response(timing)
        end_time = time.time()
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
    run_experiment("Please decide", "short")
