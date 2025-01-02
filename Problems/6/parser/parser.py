import nltk
# nltk.download('punkt_tab')
import sys
import itertools

import nltk.tokenize.api

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

"""
N V
N V Det N
N V Det N P N
N V P Det Adj N Conj N V
Det N V Det Adj N 
N V P N
N Adv V Det N Conj N V P Det N Adv
N V Adv Conj V Det N
N V Det Adj N P N Conj V N P Det Adj N
N V Det Adj Adj Adj N P Det N P Det N
N V P Det N
N V P Det Adj N
N V P Det Adj Adj N


NOT -- N P Det V N
NOT -- N V P Det Det N
"""


NONTERMINALS = """
S -> NP VP | S Conj VP | S Conj S
NP -> N | Pre N | NP Adv | NP P NP
VP -> V | V NP | V Adv
A -> Adj | Adj Adj | Adj Adj Adj
M -> Det | A | Det A
Pre -> P M | P | M
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():
    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    tokenized = nltk.tokenize.word_tokenize(sentence)

    return [w.lower() for w in tokenized if any(c.isalpha() for c in w)]


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    subtrees = list(tree.subtrees(lambda t: t.label() == "NP"))
    for a, b in itertools.combinations(subtrees, 2):
        if b in subtrees and a in subtrees:
          for c in b.subtrees(lambda t: t.label() == "NP"):
              if a == c:
                  subtrees.remove(b)
          for d in a.subtrees(lambda t: t.label() == "NP"):
              if b == d:
                  subtrees.remove(a)
                
    return subtrees


if __name__ == "__main__":
    main()
