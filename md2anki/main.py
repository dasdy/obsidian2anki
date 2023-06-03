from collections import defaultdict
from typing import Iterable

import click
from pathlib import Path
import re

from data import Word
from md2anki import anki

TRANSLATION_REGEXP = re.compile("^translation::(.*)$", re.IGNORECASE)


def word_from_file(filename: str, content: list[str]) -> Word:
    for line in content:
        if m := TRANSLATION_REGEXP.match(line):
            return Word(filename, m.group(1))

    raise ValueError(f"Bad file: {filename}")


def group_by(paths: Iterable[Path]) -> dict[str, list[Path]]:
    """
    group folders into a dict of <first_letter> -> List<filepaths>
    :param paths:
    :return:
    """
    res = defaultdict(list)
    for p in paths:
        res[p.name[0].lower()].append(p)
    return res


@click.command()
@click.option("--path", "-p", help="Input path to dir with md files", required=True)
@click.option(
    "--out", "-o", help="Output path where cards should be stored", default="out"
)
def card_pairs(path: str, out: str) -> None:
    """
    From collection of md documents, create a shorter per-letter collection of obsidian-friendly memory-repetition
    documents
    """
    filenames = Path(path).iterdir()
    groups = group_by(filenames)
    for k, g in groups.items():
        with open(f"{out}/{k}.md", "w") as outf:
            outf.write(f"#flashcards/{k}\n")
            for p in sorted(g):
                with p.open() as f:
                    w = word_from_file(p.name.rstrip(".md"), f.readlines())
                    outf.write(f"{w.word}:::?{w.translation}\n")


# TODO: add ability to pass existing pkg file to update it in-place (just adding new items)
# TODO: (2) the update should somehow honor anki's history. Maybe this should create a pkg with only new items?


@click.command()
@click.option("--path", "-p", help="Input path to dir with md files", required=True)
@click.option(
    "--out", "-o", help="Output path where cards should be stored", default="out.apkg"
)
def to_anki_base(path: str, out: str) -> None:
    filenames = Path(path).iterdir()
    words = []
    for p in filenames:
        with p.open() as f:
            w = word_from_file(p.name.removesuffix(".md"), f.readlines())
            words.append(w)
    anki.to_database(sorted(words, key=lambda wrd: wrd.word.lower()), out)


@click.group()
def cli():
    pass


cli.add_command(card_pairs)
cli.add_command(to_anki_base)


if __name__ == "__main__":
    cli()