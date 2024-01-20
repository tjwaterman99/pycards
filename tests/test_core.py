import json
from pycards import Suit, Rank, Card, Deck


def test_suits():
    assert Suit.spades == Suit.spades
    assert Suit.spades > Suit.clubs
    assert Suit.clubs > Suit.diamonds
    assert Suit.diamonds > Suit.hearts
    assert Suit.hearts == Suit.hearts
    assert Suit.hearts >= Suit.hearts


def test_ranks():
    assert Rank.king == Rank.king
    assert Rank.king > Rank.queen
    assert Rank.king >= Rank.queen


def test_card_init():
    c = Card("KH")
    assert c.suit == Suit.hearts
    assert c.rank == Rank.king

    c = Card("TC")
    assert c.suit == Suit.clubs
    assert c.rank == Rank.ten

    c = Card("2D")
    assert c.suit == Suit.diamonds
    assert c.rank == Rank.two

    c = Card("kh")
    assert c.rank == Rank.king
    assert c.suit == Suit.hearts

    c = Card.from_literal(Rank.ace, Suit.spades)
    assert c.rank == Rank.ace
    assert c.suit == Suit.spades


def test_card_ordering():
    ace_spades = Card("AS")
    ace_clubs = Card("AC")
    king_diamonds = Card("KD")
    two_diamonds = Card("2D")
    ace_hearts = Card("AH")

    assert ace_spades == ace_spades
    assert ace_spades > ace_clubs > king_diamonds > two_diamonds
    assert ace_hearts > two_diamonds


def test_card_repr():
    c = Card("kh")
    assert "KH" in repr(c)


def test_card_str():
    c = Card("as")
    assert "AS" == str(c)


def test_card_serialization():
    c = Card("as")
    assert type(c.serialize()) == str
    assert Card.deserialize(c.serialize()) == c

    # Note: round tripping is not case insensitive
    c = '"AS"'
    assert Card.deserialize(c).serialize() == c


def test_deck():
    d = Deck()
    assert len(d) == 52
    assert Card("2H") in d
    assert max(d) == Card("AS")
    assert min(d) == Card("2H")


def test_deck_draw():
    d = Deck()
    c = d.draw()
    assert c not in d


def test_deck_shuffle():
    d = Deck()
    d.sort()
    assert d.draw() == Card("AS")

    copied = list(d.cards)
    d.shuffle()
    assert d.cards != copied

    d.sort()
    assert d.cards == copied


def test_deck_serialization():
    d = Deck()
    d.draw()
    assert d == Deck.deserialize(d.serialize())

    deck = json.dumps({"cards": ["AS", "JC"]})
    assert Deck.deserialize(deck).serialize() == deck
