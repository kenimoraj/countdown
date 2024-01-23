from numbers_round_calc import get_ans_numbers, simplify, Fraction
from letters_round_calc import get_ans_letters, print_results
from datetime import datetime

N_OF_NUMBERS = 6

MIN_LETTERS = 6
MAX_LETTERS = 9
def input_int(prompt: str):
    ans = input(prompt)
    try:
        return int(ans)
    except ValueError:
        print("Wrong value. Try again")
        input_int(prompt)


def input_choice(prompt: str, choices: list):

    ext_prompt = f"{prompt} ({"|".join(choices)}) "
    ans = input(ext_prompt)
    while ans not in choices:
        print("Wrong value. Try again")
        ans = input(ext_prompt)
    return ans


def numbers_round():
    target = int(input("Pick the target number: "))

    nums = []
    print("Pick the numbers.")
    for i in range(1, N_OF_NUMBERS+1):
        nums.append(int(input(f"Number {i}: ")))

    target_frac = Fraction(target,1)
    nums_frac = [Fraction(n,1) for n in nums]
    print("Calculating...")
    start_time = datetime.now()
    ans = get_ans_numbers(target_frac, nums_frac)
    end_time = datetime.now()

    time_delta = end_time - start_time

    t = f"{time_delta.seconds}.{time_delta.microseconds // 10000}"

    if ans is not None:
        print(f"Done! All took {t} seconds.")
        print(f"{target} = {simplify(ans)}")
    else:
        print(f"Impossible. Looking through all possibilities took {t} seconds")


def letters_round():
    wordlist = []
    with open("english.txt", "r") as file:
        for line in file:
            wordlist.append(line[:-1])

    letters = input("Please type the letters as one word: ").lower()
    start_time = datetime.now()
    results = get_ans_letters(letters, wordlist)
    end_time = datetime.now()
    time_delta = end_time - start_time
    t = f"{time_delta.seconds}.{time_delta.microseconds//10000}"
    print("Done!")
    print_results(results, MIN_LETTERS, MAX_LETTERS)
    print(f"All took {t} seconds.")


try:
    ans = input_choice("Shall we play a numbers game or a letters game?", ["l", "n"])
    if ans == "n":
        numbers_round()
    else:
        letters_round()
except KeyboardInterrupt:
    pass
