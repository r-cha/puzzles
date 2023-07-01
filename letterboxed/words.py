import re
from pathlib import Path


class Words:
    """
    A class to retrieve and filter the word list.
    Defaults to unix dictionary, but will fall back to local copy if not available.
    Expects local copy to be in the same directory as this file.
    If not, falls back once more to download from remote.
    """

    default = Path("/usr/share/dict/words")
    local = Path(__file__).parent / "words"
    remote = "https://svnweb.freebsd.org/csrg/share/dict/words?view=co"

    _minimum_length = 3

    def __init__(self):
        if self.default.exists():
            self.path = self.default
        elif self.local.exists():
            self.path = self.local
        else:
            self._download(self.remote, self.local)
            self.path = self.local

        self.text = self.path.read_text().lower().strip()

    def _download(self, remote_path, local_path):
        import requests

        response = requests.get(remote_path)
        local_path.write_text(response.text)

    def filter(self, sides):
        """
        Filter the complete word list down to only those allowed.

        :param sides: The four three-letter groupings present on the game board.
        :return: A list of words that can be used to solve the puzzle.
        """

        pattern = (
            "^(?:" + "|".join(f"(?:(?<![{side}])[{side}])" for side in sides) + ")*$"
        )
        return [
            word
            for word in re.findall(
                pattern, self.text, flags=re.MULTILINE | re.IGNORECASE
            )
            if len(word) >= self._minimum_length
        ]


if __name__ == "__main__":
    """Download the word list if manually invoked."""
    Words()._download(Words.remote, Words.local)
