import html

import genanki
import random

from data import Word


def to_database(words: list[Word], path: str):
    model_id = random.randrange(1 << 30, 1 << 31)
    model = genanki.Model(
        model_id,
        "Words Model",
        fields=[
            {"name": "Question"},
            {"name": "Answer"},
        ],
        templates=[
            {
                "name": "Card 1",
                "qfmt": "{{Question}}",
                "afmt": '{{FrontSide}}<hr id="answer">{{Answer}}',
            },
        ],
    )

    deck = genanki.Deck(random.randrange(1 << 30, 1 << 31), "Obsidian Czech vocab")
    for w in words:
        w_fields = [html.escape(w.word), html.escape(w.translation)]
        print(f"{w.word} -> {w_fields}")
        deck.add_note(genanki.Note(model=model, fields=w_fields))

    deck.write_to_file(path)
