from typing import List


def user_confirmation(prompt: str) -> bool:
    answer = input(prompt)
    return answer.lower() in ("y", "yes")


def user_choice(choices: List[str]) -> str:
    for i, choice in enumerate(choices):
        print(f"{i+1}: {choice}")

    selection = int(input("Choice: "))

    return choices[selection - 1]
