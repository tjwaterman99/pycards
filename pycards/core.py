from enum import Enum


class Suit(Enum):
    spades = 'S'
    clubs = 'C'
    diamonds = 'D'
    hearts = 'H'    

    def __eq__(self, other: 'Suit'):
        return self.value == other.value
    
    def __gt__(self, other: 'Suit'):
        return self._member_names_.index(self.name) < self._member_names_.index(other.name)
    
    def __ge__(self, other: 'Suit'):
        return self == other or self > other


class Rank(Enum):
    ace = 'A'
    king = 'K'
    queen = 'Q'
    jack = 'J'
    ten = 'T'
    nine = '9'
    eight = '8'
    seven = '7'
    six = '6'
    five = '5'
    four = '4'
    three = '3'
    two = '2'

    def __eq__(self, other: 'Rank'):
        return self.value == other.value
    
    def __gt__(self, other: 'Rank'):
        return self._member_names_.index(self.name) < self._member_names_.index(other.name)

    def __ge__(self, other: 'Rank'):
        return self == other or self > other


class Card:
    def __init__(self, value: str):
        if type(value) != str:
            raise ValueError(f"Card must be initialized with a string, received: {str(type(value))}")
        if len(value) != 2:
            raise ValueError(f"Card must be initialized with a suit and rank, like `2H` or `AD`. Received: {str(value)}")
        rank, suit = value
        self.suit = Suit(suit)
        self.rank = Rank(rank)
