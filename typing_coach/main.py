import random

from key_runner import KeyRunner


def get_random_phrase():
    phrases = []
    with open('data.txt', 'r') as f:
        while True:
            a = f.readline()
            if not a:
                break
            b = f.readline()
            c = f.readline()
            phrases.append((a, b))
    return phrases[random.randint(0, len(phrases))][1]


def main():
    KeyRunner(get_random_phrase()).start()


if __name__ == '__main__':
    main()
