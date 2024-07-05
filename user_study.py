import json
import sys
import termios
import threading
import time
import msvcrt
import tty
import uuid

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

    timer_thread = threading.Thread(target=timer)
    timer_thread.start()

    try:
        tty.setraw(sys.stdin.fileno())
        while not response['answered']:
            key = sys.stdin.read(3)
            if key == '\x1b[D':  # Left arrow key code
                response = {'answered': True, 'response': 'A'}
            elif key == '\x1b[C':  # Right arrow key code
                response = {'answered': True, 'response': 'B'}
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    return response['response'] == "A"


def save_responses(responses, filename):
    with open(filename, 'w') as file:
        json.dump(responses, file, indent=4)


def run_experiment(instructions, mode="long", ai_model=None):
    assert mode in ["long", "short", "ai"], "Provided mode needs to be either long, short or ai"

    dataset = Dataset()
    user_responses = []

    participant_id = input("Please enter your participant ID: ")
    unique_session_id = str(uuid.uuid4())
    print(f"Thanks for joining {participant_id}. Your unique session ID: {unique_session_id}")

    if mode in ["short", "ai"]:


    for problem in dataset:
        choiceA, choiceB = problem["A"], problem["B"]

        print(instructions)
        print(f"A (left): {choiceA}\t\tvs.\t\tB (right): {choiceB}")

        # get the user's answer
        start_time = time.time()
        response = get_user_response()
        end_time = time.time()
        guts_feeling_timing = end_time - start_time

        # provide the user with a recommendation, if ai model is provided
        if ai_model is not None:
            # todo add a time limit for accepting the AI suggestion
            recommendation = ai_model.evaluate_problem([choiceA, choiceB])

            if recommendation == 0:
                pass
            #todo feedback to the user by the AI

            start_time = time.time()
            response = get_user_response()
            end_time = time.time()
            after_ai_rec_timing = end_time - start_time

            # present both outcomes of feedback

        user_responses.append({'problem': problem["Problem"], 'response': response, 'guts_feeling_timing': guts_feeling_timing})

    save_responses(user_responses, 'responses_.json')


if __name__ == "__main__":
    main()
