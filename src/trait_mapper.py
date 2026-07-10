import csv
import re


class TraitMapper:
    def __init__(self, traits_path, aliases_path):
        self.aliases = {}
        self.names = {}
        with open(aliases_path, encoding="utf-8-sig", newline="") as handle:
            for row in csv.DictReader(handle):
                self.aliases[self._normalise(row["alias"])] = row["traitId"]
        with open(traits_path, encoding="utf-8-sig", newline="") as handle:
            for row in csv.DictReader(handle):
                self.names[self._normalise(row["name"])] = row["id"]

    @staticmethod
    def _normalise(value):
        return re.sub(r"\s+", "", value or "").strip()

    def map(self, value):
        key = self._normalise(value)
        return self.aliases.get(key) or self.names.get(key)

    def find_in_text(self, value):
        text = self._normalise(value)
        found = []
        # Long names first prevents an individual character matching prematurely.
        candidates = {**self.names, **self.aliases}
        for label, trait_id in sorted(candidates.items(), key=lambda item: len(item[0]), reverse=True):
            if label and label in text and trait_id not in found:
                found.append(trait_id)
        return found
