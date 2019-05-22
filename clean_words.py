
def main():
    with open('words_clean.txt', 'w') as g:
        with open('words_alpha.txt', 'r') as f:
            for line in f:
                line = line.lower().strip()
                if len(line) >= 3:
                    g.write(line + '\n')


if __name__ == '__main__':
    main()
