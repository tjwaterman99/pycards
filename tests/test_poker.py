from pycards import Deck, Suit
from pycards.poker import Hand


def test_hand_has_straight():
    d = Deck()
    d.sort()
    h = Hand(*[c for c in d if c.suit == Suit.spades][:5])
    assert h.has_straight()


def test_hand_tier():
    d = Deck()
    d.sort()
    h = Hand(*d[:5])
    assert h.tier() is not None
