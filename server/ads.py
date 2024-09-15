from __future__ import annotations

import json
import os
import string
import random

dirname = os.path.dirname(__file__)
ads_file = os.path.join(dirname, "data/ads.json")

alphabet = string.ascii_lowercase + string.digits


def generate_random_id() -> str:
    return "".join(random.choices(alphabet, k=8))


def clean_str(s: str) -> str:
    return "".join(c if c.isalnum() else " " for c in s.lower())


class AdsBank:
    """
    Stores ad information in `self.ads` (a dict mapping unique ad ids to ad info dicts)
    and has a `self.kw_lookup` for quickly finding an ad that has a keyword associated with it.
    """

    def __init__(self) -> None:
        self.ads = {}
        self.kw_lookup = {}
        self.read()

    def read(self):
        if not os.path.exists(ads_file):
            self.write()
            return

        with open(ads_file) as f:
            data = json.load(f)

        self.ads = data["ads"]
        self.kw_lookup = data["kw_lookup"]

    def write(self):
        with open(ads_file, "w") as f:
            json.dump({"ads": self.ads, "kw_lookup": self.kw_lookup}, f)

    def add_ad(self, message: str, img_url: str, keywords: str | list[str]):
        uid = generate_random_id()
        while uid in self.ads:
            # Ensure uniqueness
            uid = generate_random_id()

        self.ads[uid] = {
            "uid": uid,
            "message": message,
            "img_url": img_url,
            "keywords": keywords,
        }

        if isinstance(keywords, str):
            keywords = [keywords]

        for kw in keywords:
            self.kw_lookup[clean_str(kw)] = uid

        self.write()

    def select_ad(self, question: str, history: list[str]) -> tuple[str, str] | None:
        for word in clean_str(question).split():
            if word in self.kw_lookup:
                return self.ads[self.kw_lookup[word]]

        return None


if __name__ == "__main__":
    # Sets up new ads
    # Usage: python ads.py message img_url keywords+
    # Note: img_url can either be a file relative to the public/ dir or a web url to an online image
    import sys

    if len(sys.argv) < 4:
        raise ValueError(
            "Invalid usage. Usage: python ads.py message img_url_relative_to_public_dir keywords+"
        )

    ads_bank = AdsBank()
    ads_bank.add_ad(sys.argv[1], sys.argv[2], sys.argv[3:])
