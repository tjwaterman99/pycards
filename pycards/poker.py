from collections import Counter
from pycards.core import Card, OrderedEnum


class HandTier(OrderedEnum):
    straight_flush = 0
    four_kind = 1
    full_house = 2
    flush = 3
    straight = 4
    three_kind = 5
    two_pair = 6
    pair = 7
    highcard = 8


class Hand:
    def __init__(self, *cards: list[Card]):
        if len(cards) != 5:
            raise ValueError(
                f"A hand must be composed of 5 cards, received {len(cards)}"
            )
        self.cards: list[Card] = list(sorted(cards))  # type: ignore
        self.suits = Counter((c.suit for c in self.cards))
        self.ranks = Counter((c.rank for c in self.cards))

    def tier(self):
        if len(self.ranks) == 2:
            if max(self.ranks.values()) == 4:
                return HandTier.four_kind
            else:
                return HandTier.full_house
        elif len(self.ranks) == 3:
            if max(self.ranks.values()) == 3:
                return HandTier.three_kind
            else:
                return HandTier.two_pair
        elif len(self.ranks) == 4:
            return HandTier.pair
        # Either a flush or straight flush
        elif len(self.suits) == 1:
            if self.has_straight():
                return HandTier.straight_flush
            else:
                return HandTier.flush
        # Either a straight or a high card
        else:
            if self.has_straight():
                return HandTier.straight
            else:
                return HandTier.highcard

    def has_straight(self):
        first_card, second_card = self.cards[:2]  # Assumes cards have been sorted
        first_rank, second_rank = first_card.rank, second_card.rank
        first_index = first_rank.__class__._member_names_.index(first_rank.name)
        second_index = second_rank.__class__._member_names_.index(second_rank.name)
        return first_index == second_index + 1
