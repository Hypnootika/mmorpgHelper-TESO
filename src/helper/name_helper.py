import requests
import random
import json
from typing import Tuple, List
from pathlib import Path

word_combinations_path = Path("D:\\Dev\\TESO\\assets\\words\\words.json")


def fetch_words() -> List[Tuple[str, str]]:
    url = "https://raw.githubusercontent.com/first20hours/google-10000-english/master/google-10000-english.txt"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to retrieve data: {response.status_code}")
    words = [word for word in response.text.split() if len(word) > 3]
    return [random.sample(words, 2) for _ in range(10)]


def save_word_combinations(combinations: List[Tuple[str, str]]):
    with word_combinations_path.open("w") as file:
        json.dump(combinations, file)


def load_word_combinations() -> List[Tuple[str, str]]:
    if word_combinations_path.exists() and word_combinations_path.stat().st_size != 0:
        with word_combinations_path.open() as file:
            return json.load(file)
    return []


def get_word_pair() -> Tuple[str, str]:
    combinations = load_word_combinations()
    if not combinations:
        combinations = fetch_words()
    _word_pair = combinations.pop(0)
    save_word_combinations(combinations)
    return _word_pair


def format_words(_word_pair: Tuple[str, str]) -> str:
    word1, word2 = _word_pair
    return f"{word1}_{word2}.1.{random.randint(1, 20)}.{random.randint(1, 9)}"


if __name__ == "__main__":
    word_pair = get_word_pair()
    formatted_string = format_words(word_pair)
    print(formatted_string)
