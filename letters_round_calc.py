def get_ans_letters(letters: str, wordlist: list):

    result = []
    if len(wordlist) == 0:
        return None
    if "" in wordlist:
        result.append("")
        wordlist = [w for w in wordlist if w!=""]

    letter_list = [l for l in letters]

    for l in set(letter_list):
        letters_c = letter_list.copy()
        trunc = [w[1:] for w in wordlist if w[0] == l]
        letters_c.remove(l)
        prev = get_ans_letters("".join(letters_c), trunc)
        if prev is None:
            continue
        for p in prev:
            result.append(l+p)
    return result


def print_results(results: list, minletters: int, maxletters: int):
    for i in range(maxletters, minletters - 1, -1):
        print(f"{i}-letter words: {", ".join([r for r in results if len(r) == i])}")
