"""
Contains the entities used in the game
"""

import random

SUITS = ("Hearts", "Diamonds", "Spades", "Clubs")
RANKS = {"Two": 2, "Three": 3, "Four": 4, "Five": 5, "Six": 6, "Seven": 7, "Eight": 8,
            "Nine": 9, "Ten": 10, "Jack": 10, "Queen": 10, "King": 10, "Ace": {"min": 1, "max": 11}}


class Card:
    """
    Card used in the game

    Atributes
    - suit: str - suit of the card
    - rank: str - rank of the card
    """

    def __init__(self, suit: str, rank: str) -> None:
        """
        Parameters
        suit: str
            Suit of the card (use values in SUITS)
        rank: str
            Rank of the card (use values in RANKS)
        """

        self.suit = suit
        self.rank = rank

    def __str__(self) -> str:
        return f"{self.rank} of {self.suit}"


class Deck:
    """
    Deck containing all 52 cards
    """

    def __init__(self) -> None:
        self.cards = []
        for suit in SUITS:
            for rank in RANKS.keys():
                self.cards.append( Card(suit, rank) )

    def __len__(self) -> int:
        return self.cards.__len__()

    def shuffle(self) -> None:
        """
        Shuffles the cards in the deck
        """

        random.shuffle(self.cards)

    def deal(self) -> Card:
        """
        Deals one card off the deck

        Returns
        The card removed
        """

        return self.cards.pop()


class HandIter:
    """
    Iterator for the class Hand
    """

    def __init__(self, hand):
        self.cards = hand.cards
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.cards):
            output = self.cards[self.index]
            self.index += 1
            return output
        else:
            raise StopIteration


class Hand:
    """
    Hand of cards

    Atributes
    - total: int - sum of the rank values

    Methods
    - add(self, card: Card) -> None
    - adjust_for_aces(self) -> None
    """

    def __init__(self) -> None:
        self.cards = []
        self.total = 0
        self.aces_to_adjust = 0

    def __iter__(self):
        return HandIter(self)

    def __len__(self):
        return len(self.cards)

    def __str__(self) -> str:
        output = ""
        if len(self.cards) > 0:
            index = 0
            output += str(self.cards[index])
            index += 1
            while index < len(self.cards):
                output += f", {self.cards[index]}"
                index += 1
        return output

    def add(self, card: Card) -> None:
        """
        Adds a card to the hand

        Parameters
        - card: Card - card to be added
        """

        self.cards.append(card)
        if card.rank == "Ace":
            self.total += RANKS[card.rank]["max"]
            self.aces_to_adjust += 1
        else:
            self.total += RANKS[card.rank]

    def adjust_for_aces(self) -> None:
        """
        Adjusts the value of the aces to unbust the hand's owner
        """

        while self.aces_to_adjust > 0 and self.total > 21:
            self.aces_to_adjust -= 1
            self.total -= RANKS["Ace"]["max"]
            self.total += RANKS["Ace"]["min"]
