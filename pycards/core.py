import json
import random
from typing import Iterable
from enum import Enum
from itertools import product


class OrderedEnum(Enum):
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, OrderedEnum):
            raise NotImplementedError
        return bool(self.value == other.value)

    def __gt__(self, other: "OrderedEnum") -> bool:
        return self.__class__._member_names_.index(
            self.name
        ) < self.__class__._member_names_.index(other.name)

    def __ge__(self, other: "OrderedEnum") -> bool:
        return self == other or self > other

    # TODO this doesn't need to live here
    def __str__(self) -> str:
        return str(self.value)

    def __hash__(self) -> int:
        return hash(str(self))


# Needs 2 bits
class Suit(OrderedEnum):
    spades = "S"
    clubs = "C"
    diamonds = "D"
    hearts = "H"


# Needs 4 bits to serialize efficiently
class Rank(OrderedEnum):
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


class Card:
    @classmethod
    def from_literal(cls, rank: Rank, suit: Suit) -> "Card":
        value = f"{rank}{suit}"
        return Card(value)

    def __init__(self, value: str):
        parsed = self.parse(value)
        self.rank = Rank(parsed[0])
        self.suit = Suit(parsed[1])

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Card):
            raise NotImplementedError
        return bool(self.rank == other.rank and self.suit == other.suit)

    def __gt__(self, other: "Card") -> bool:
        return self.rank > other.rank or (
            self.rank == other.rank and self.suit > other.suit
        )

    def __ge__(self, other: "Card") -> bool:
        return self == other or self > other

    def __repr__(self) -> str:
        return f"<Card '{self.rank}{self.suit}'>"

    def __str__(self) -> str:
        return f"{self.rank}{self.suit}"

    def __hash__(self) -> int:
        return hash(str(self))

    def parse(self, value: str) -> tuple[Rank, Suit]:
        if type(value) != str:
            raise ValueError(
                f"Card must be initialized with a string, received: {str(type(value))}"
            )
        if len(value) != 2:
            raise ValueError(
                f"Card must be initialized with a suit and rank, like `2H` or `AD`. Received: {str(value)}"
            )
        fvalue = value.upper()
        rank = fvalue[0]
        suit = fvalue[1]
        return Rank(rank), Suit(suit)

    def serialize(self) -> str:
        return json.dumps(str(self))

    @classmethod
    def deserialize(cls, value: str) -> "Card":
        return cls(json.loads(value))


class Deck:
    _all_cards = tuple(sorted(Card(f"{r}{s}") for s, r in product(Suit, Rank)))

    def __init__(self, shuffle: bool = True) -> None:
        self.cards = list(self._all_cards)
        if shuffle:
            self.shuffle()

    def __len__(self) -> int:
        return len(self.cards)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Deck):
            raise NotImplementedError
        if len(self) != len(other):
            return False
        # TODO: the type checking here isn't working with error:
        # > error: No overload variant of "zip" matches argument types "Deck", "Deck"  [call-overload]
        for c1, c2 in zip(self, other):  # type: ignore
            if c1 != c2:
                return False
        return True

    def __contains__(self, value: Card) -> bool:
        return value in self.cards

    def __iter__(self) -> Iterable[Card]:
        for card in self.cards:
            yield card

    def __getitem__(self, index: int) -> Card:
        return self.cards[index]

    def __repr__(self) -> str:
        return f"<Deck [{len(self)} cards]>"

    def draw(self) -> Card:
        return self.cards.pop()

    def sort(self) -> None:
        self.cards = list(sorted(self.cards))

    def shuffle(self) -> None:
        random.shuffle(self.cards)

    def serialize(self) -> str:
        container = {"cards": [str(c) for c in self.cards]}
        return json.dumps(container)

    @classmethod
    def deserialize(cls, value: str) -> "Deck":
        parsed = json.loads(value)
        cards = [Card(c) for c in parsed["cards"]]
        return cls.from_cards(cards=cards)

    @classmethod
    def from_cards(cls, cards: list[Card]) -> "Deck":
        deck = cls(shuffle=False)
        deck.cards = cards
        return deck
