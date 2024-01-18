from pycards import Suit, Rank, Card


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
    c = Card('KH')
    assert c.suit == Suit.hearts
    assert c.rank == Rank.king

    c = Card('TC')
    assert c.suit == Suit.clubs
    assert c.rank == Rank.ten

    c = Card('2D')
    assert c.suit == Suit.diamonds
    assert c.rank == Rank.two
