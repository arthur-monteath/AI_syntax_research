import csv
import random
from collections import defaultdict
from nltk.corpus import wordnet as wn


def load_lexicon_from_wordnet(
    max_per_category=2000,
    drop_multiword=True,
    min_count=1
):
    """
    Load a frequency-sorted lexicon from WordNet.

    Args:
        max_per_category (int): cap per POS
        drop_multiword (bool): remove words with underscores
        min_count (int): minimum lemma frequency to include

    Returns:
        dict[str, list[str]]
    """
    pos_map = {
        "N": wn.NOUN,
        "V": wn.VERB,
        "A": wn.ADJ,
        "Adv": wn.ADV,
    }

    lexicon = {}

    for category, wn_pos in pos_map.items():
        freq = defaultdict(int)

        for synset in wn.all_synsets(wn_pos):
            for lemma in synset.lemmas():
                word = lemma.name().lower()

                if drop_multiword and "_" in word:
                    continue

                freq[word] += lemma.count()

        # Filter + sort by frequency
        words = [
            w for w, c in freq.items()
            if c >= min_count
        ]

        words.sort(key=lambda w: freq[w], reverse=True)

        lexicon[category] = words[:max_per_category]

    return lexicon


class Tree:
    def __init__(self, label, children=None):
        self.label = label
        self.children = children or []


def load_lexicon(path):
    # Fetching from wordnet
    lexicon = load_lexicon_from_wordnet(max_per_category=1000)

    # Reading from CSV
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cat = row["category"]
            if cat in {"D", "P"}:
                lexicon.setdefault(cat, [])
                lexicon[cat].append(row["word"].lower())

    return dict(lexicon)


LEXICON = load_lexicon("lexicon.csv")


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


def weighted_choice(options):
    items, weights = zip(*options)
    return random.choices(items, weights=weights, k=1)[0]


def generate_tree(node):
    # Terminal symbol
    if node in LEXICON:
        return Tree(random.choice(LEXICON[node]))

    # Non-terminal
    if node in GRAMMAR:
        expansion = weighted_choice(GRAMMAR[node])
        children = [generate_tree(child) for child in expansion]
        return Tree(node, children)
    
    return Tree("")


def linearize(tree):
    if not tree.children:
        return tree.label
    return " ".join(linearize(c) for c in tree.children)