import dataclasses as dc


@dc.dataclass
class Word:
    word: str
    translation: str
