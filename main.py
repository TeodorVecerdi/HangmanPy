words = []
word_length = 1
mistakes = 0
max_mistakes = 5
min_chars = 3
max_chars = 15
found_word = False
game_running = False
game_lost = False
guess = []
alphabet = []
weights = []


def check_word(word):
    global guess, alphabet
    if not word.isalpha() or len(word) != len(guess):
        return False
    for i in range(26):
        if alphabet[i] == 'x':
            char = chr(i+ord('a'))
            for j in range(len(word)):
                if guess[j] != char and word[j] == char:
                    return False
        if alphabet[i] == '.' and chr(i + ord('a')) in word:
            return False

    for i in range(len(guess)):
        if guess[i] != '.':
            if guess[i] != word[i]:
                return False
    return True


def reset_game():
    global word_length, mistakes, found_word, game_running, guess, alphabet, weights, min_chars, max_chars
    word_length = 1
    mistakes = 0
    found_word = False
    game_running = True
    alphabet = list('abcdefghijklmnopqrstuvwxyz')
    weights = [0.0 for i in range(26)]

    while word_length < min_chars or word_length > max_chars:
        word_length = int(
            input('Enter the length of your word. (Between {} and {} characters): '.format(min_chars, max_chars)))
        if word_length < min_chars or word_length > max_chars:
            print('Word length must be between {} and {} characters'.format(min_chars, max_chars))

    guess = ['.' for i in range(word_length)]


def reload_words():
    global words
    words = []

    with open('words_clean.txt') as f:
        for word in f:
            word = word.lower().strip()
            if check_word(word):
                words.append(word)


def calculate_weights():
    global weights, alphabet, guess
    weights = [0.0 for i in range(26)]
    totals = [0 for i in range(26)]
    total = 0
    for word in words:
        for char in word:
            if char not in guess:
                total += 1
                totals[ord(char) - ord('a')] += 1
    for i in range(26):
        if alphabet[i] == '.' or alphabet[i] == 'x':
            weights[i] = -1.0
            continue
        weights[i] = (totals[i] / total) * 100.0


def make_choice():
    global weights
    max_weight = max(weights)
    index = weights.index(max_weight)
    choice = alphabet[index]
    alphabet[index] = '.'
    return choice


# m  o  t  h  e  r
# 1  2  3  4  5  6  7  8  9  10 11 12 13 14 15
def main():
    global game_running, found_word, mistakes, word_length, guess, game_lost, max_mistakes
    reset_game()
    reload_words()
    calculate_weights()
    print('Total words: {}'.format(len(words)))
    while game_running:
        choice = make_choice()
        is_choice_correct = input('Does your word contain \'{}\'? y/n: '.format(choice))
        if is_choice_correct.lower() == 'y':
            locations = [int(loc) for loc in
                         input('Enter the character \'{}\' in your word (1-{}): '.format(choice, word_length)).split(
                             ' ')]
            for loc in locations:
                guess[loc - 1] = choice
            alphabet[ord(choice) - ord('a')] = 'x'
            reload_words()
            if '.' in guess and len(words) != 0:
                calculate_weights()
        elif is_choice_correct.lower() == 'n':
            mistakes += 1
            reload_words()
            calculate_weights()
            print('{} mistake{} left'.format(str(max_mistakes - mistakes), 's' if max_mistakes - mistakes != 1 else ''))

        if len(words) == 0:
            print("I could not guess your word.")
            game_lost = True
            game_running = False
            break
        if '.' not in guess or len(words) == 1:
            print('\nI think \'{}\' is your word'.format(''.join(words[0] if len(words) == 1 else guess)))
            game_running = False
            break
        else:
            print('Current guess: {}; Remaining words: {}'.format(''.join(guess), len(words)))
            # if len(words) < 20:
            #     print(words)

        if mistakes >= max_mistakes:
            print("I could not guess your word.")
            game_lost = True
            game_running = False
            break

        if found_word:
            game_running = False
    if game_lost:
        print('Words left: {}'.format(words))


if __name__ == '__main__':
    main()
