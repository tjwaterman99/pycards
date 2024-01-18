import random
from enum import Enum
from itertools import product
from typing import Union


class Suit(Enum):
    spades = "S"
    clubs = "C"
    diamonds = "D"
    hearts = "H"

    def __eq__(self, other: "Suit"):
        return self.value == other.value

    def __gt__(self, other: "Suit"):
        return self._member_names_.index(self.name) < self._member_names_.index(
            other.name
        )

    def __ge__(self, other: "Suit"):
        return self == other or self > other

    def __str__(self):
        return self.value


class Rank(Enum):
    ace = "A"
    king = "K"
    queen = "Q"
    jack = "J"
    ten = "T"
    nine = "9"
    eight = "8"
    seven = "7"
    six = "6"
    five = "5"
    four = "4"
    three = "3"
    two = "2"

    def __eq__(self, other: "Rank") -> bool:
        return self.value == other.value

    def __gt__(self, other: "Rank") -> bool:
        return self._member_names_.index(self.name) < self._member_names_.index(
            other.name
        )

    def __ge__(self, other: "Rank") -> bool:
        return self == other or self > other

    def __str__(self):
        return self.value


class Card:
    @classmethod
    def from_literal(cls, rank: Rank, suit: Suit) -> "Card":
        value = f"{rank}{suit}"
        return Card(value)

    def __init__(self, value: str):
        if type(value) != str:
            raise ValueError(
                f"Card must be initialized with a string, received: {str(type(value))}"
            )
        if len(value) != 2:
            raise ValueError(
                f"Card must be initialized with a suit and rank, like `2H` or `AD`. Received: {str(value)}"
            )
        rank, suit = value.upper()
        self.suit = Suit(suit)
        self.rank = Rank(rank)

    def __eq__(self, other: "Card") -> bool:
        return self.rank == other.rank and self.suit == other.suit

    def __gt__(self, other: "Card") -> bool:
        return self.rank > other.rank or (
            self.rank == other.rank and self.suit > other.suit
        )

    def __ge__(self, other: "Card") -> bool:
        return self == other or self > other

    def __repr__(self):
        return f"<Card '{self.rank}{self.suit}'>"

    def __str__(self):
        return f"{self.rank}{self.suit}"

    def __hash__(self):
        return hash(str(self))


cards = frozenset([Card(f"{r}{s}") for s, r in product(Suit, Rank)])
"""
A frozenset of all cards
"""


class Deck:
    _all_cards = cards

    def __init__(self, shuffle=True):
        self.cards = list(self._all_cards)
        if shuffle:
            self.shuffle()

    def __len__(self):
        return len(self.cards)

    def __contains__(self, value: Card):
        return value in self.cards

    def __iter__(self):
        for card in self.cards:
            yield card

    def draw(self) -> Card:
        return self.cards.pop()

    def sort(self) -> None:
        self.cards = list(sorted(self.cards))

    def shuffle(self) -> None:
        random.shuffle(self.cards)
