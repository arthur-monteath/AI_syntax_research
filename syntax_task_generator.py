import random

LEXICON = {
    "N": ["dog", "cat", "man", "woman", "child"],
    "V": ["chases", "sees", "likes", "hates"],
    "D": ["the", "a", "every", "some"],
    "P": ["with", "without", "on", "under"],
    "A": ["big", "small", "red", "blue"],
    "Adv": ["quickly", "slowly", "happily", "sadly"],
}


# XP, X', and X and their possible children
GRAMMAR = {
    "S": [
        (["NP", "VP"], 1.0)
    ],

    "NP": [
        (["D", "N'"], 0.7),
        (["N'"], 0.3),
    ],

    "N'": [
        (["N"], 0.4),
        (["A", "N'"], 0.35),
        (["N", "PP"], 0.25),
    ],

    "VP": [
        (["V"], 0.25),
        (["V", "NP"], 0.45),
        (["V", "NP", "PP"], 0.2),
        (["Adv", "VP"], 0.1),
    ],

    "PP": [
        (["P", "NP"], 1.0)
    ],
}


def uniform_choice(options):
    return random.choice(options)


def weighted_choice(options):
    items, weights = zip(*options)
    return random.choices(items, weights=weights, k=1)[0]


def generate(node):
    # Terminal symbol
    if node in LEXICON:
        return uniform_choice(LEXICON[node])

    # Non-terminal
    if node in GRAMMAR:
        expansion = weighted_choice(GRAMMAR[node])
        return " ".join(generate(child) for child in expansion)

    # Fallback
    return ""


def generate_sentence():
    sentence = generate("S")
    return sentence.capitalize() + "."


print(generate_sentence())