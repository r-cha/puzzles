import argparse

import networkx as nx

from words import Words


def build_graph(letters, words):
    # Weight is the potential of that transition,
    # i.e. the number of letters that would be left to cover if we chose that word.
    G = nx.DiGraph()
    G.add_node(0)
    for word in words:
        wordset = set(word)
        remaining = letters - wordset
        G.add_edge(0, word, weight=len(remaining))
        for other_word in words:
            if word == other_word:
                continue
            if word[-1] == other_word[0]:
                potential_remaining = set(other_word) - wordset
                G.add_edge(word, other_word, weight=len(potential_remaining))
    return G


def find_shortest_path(G: nx.Graph, letters: set[str], depth=3) -> list[str]:
    bests = []
    for other_node in G.nodes:
        if other_node == 0:
            continue
        possibilities = []
        for path in nx.all_simple_paths(G, 0, other_node, depth):
            path.remove(0)
            if len(letters - set("".join(path))) == 0:
                possibilities.append(path)
        if possibilities:
            bests.append(min(possibilities, key=len))
    return sorted(bests, key=lambda path: len("".join(path)), reverse=True)


def main(sides, depth):
    letters = set("".join(sides))

    print("Generating wordlist")
    words = Words().filter(sides)

    print("Building graph")
    graph = build_graph(letters, words)
    print("Weighing options")
    shortest = find_shortest_path(graph, letters, depth=depth)

    print("Solution(s): (q to quit)")
    while shortest:
        print(shortest.pop(), end="")
        if input() == "q":
            break
    print("Done")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Find the shortest covering string of a set of letters."
    )
    parser.add_argument(
        "sides",
        metavar="S",
        type=str,
        nargs="*",
        help="A side of the letter box. Expects 4 3-letter arguments.",
        default=["uhx", "eon", "kim", "crb"],
    )
    parser.add_argument(
        "--depth",
        type=int,
        help="The maximum pathlength to consider.",
        default=3,
    )
    args = parser.parse_args()
    main(args.sides, args.depth)
