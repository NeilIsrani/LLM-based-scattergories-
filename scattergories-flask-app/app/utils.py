import random


def roll_die():
    import random
    return random.randint(1, 20)

def generate_prompts():
    prompts = [
        "Name a fruit",
        "Name a country",
        "Name a movie",
        "Name a color",
        "Name an animal",
        "Name a city",
        "Name a song",
        "Name a book",
        "Name a sport",
        "Name a vegetable"
    ]
    return random.sample(prompts, 3)  # Select 3 random prompts

def start_timer(duration):
    import time
    time.sleep(duration)  # Simulate a timer for the given duration in seconds

def calculate_score(answers, correct_answers):
    score = 0
    for answer in answers:
        if answer in correct_answers:
            score += 1
    return score