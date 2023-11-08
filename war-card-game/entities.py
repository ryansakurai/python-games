import random
from typing import Iterable

SUITS = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
RANKS = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
NUM_VALUES = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8,
            'Nine': 9, 'Ten': 10, 'Jack': 11, 'Queen': 12, 'King': 13, 'Ace': 14}


class Card:
    def __init__(self, suit: str, rank: str) -> None:
        self.suit = suit.capitalize()
        self.rank = rank.capitalize()

    def __str__(self) -> str:
        return f"{self.rank} of {self.suit}"


class Deck:
    def __init__(self) -> None:
        self._cards = []

    def __len__(self) -> int:
        return len(self._cards)

    def shuffle(self) -> None:
        random.shuffle(self._cards)

    def add_cards(self, card: Card | Iterable[Card]) -> None:
        ## single card
        if type(card) == Card:
            self._cards.append(card)

        ## iterable of cards
        else:
            self._cards.extend(card)

    def remove_card(self) -> Card:
        return self._cards.pop(0)


class FullDeck(Deck):
    """
    Deck holding all 52 cards
    """

    def __init__(self) -> None:
        super().__init__()
        for suit in SUITS:
            for rank in RANKS:
                self._cards.append( Card(suit, rank) )

    def add_cards(*args):
        """
        Not used
        """

        pass


class Player:
    def __init__(self, name: str) -> None:
        self._deck = Deck()
        self.name = name
        self.rounds_won = 0

    def __len__(self) -> int:
        return len(self._deck)

    def __str__(self) -> str:
        return f"{self.name}: {self.rounds_won} rounds won"

    def add_cards(self, card: Card | Iterable[Card]) -> None:
        self._deck.add_cards(card)

    def remove_card(self) -> Card:
        return self._deck.remove_card()

    def win_round(self) -> None:
        self.rounds_won += 1


def compare(first: Card, second: Card) -> int:
    """
    Returns
    - A positive number, if the first card is the greater
    - A negative number, if the first card is the least
    - Zero, if the first card is equal to the second card
    """

    return NUM_VALUES[first.rank] - NUM_VALUES[second.rank]
