import re
from pathlib import Path

import networkx as nx


def load_words(letters: list[str]) -> list[str]:
    f = Path("/usr/share/dict/words").read_text()
    pattern = "^(?:" + "|".join(f"(?:(?<![{set}])[{set}])" for set in letters) + ")*$"
    return re.findall(pattern, f, flags=re.MULTILINE | re.IGNORECASE)


def solve(words, letters):
    remaining_chars = set(letters)
    selected_words = []
    while remaining_chars:
        best_word = max(words, key=lambda word: len(set(word) & remaining_chars))
        selected_words.append(best_word)
        remaining_chars -= set(best_word)
    for i in range(len(selected_words) - 1):
        print(selected_words[i], selected_words[i + 1])


def dfs(graph, visited, path, node):
    visited.add(node)
    path.append(node)
    for neighbor in graph.neighbors(node):
        if neighbor not in visited:
            dfs(graph, visited, path, neighbor)


def main():
    letters = ["uhx", "eon", "kim", "crb"]
    words = load_words(letters)
    solve(words, letters)


if __name__ == "__main__":
    main()
