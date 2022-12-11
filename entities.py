import random

SUITS = ("Hearts", "Diamonds", "Spades", "Clubs")
RANKS = {"Two": 2, "Three": 3, "Four": 4, "Five": 5, "Six": 6, "Seven": 7, "Eight": 8,
            "Nine": 9, "Ten": 10, "Jack": 10, "Queen": 10, "King": 10, "Ace": {"min": 1, "max": 11}}


class Card:
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
        self._cards = []
        for suit in SUITS:
            for rank in RANKS.keys():
                self._cards.append( Card(suit, rank) )

    def __len__(self) -> int:
        return self._cards.__len__()

    def shuffle(self) -> None:
        random.shuffle(self._cards)

    def deal(self) -> Card:
        return self._cards.pop()


class HandIter:
    def __init__(self, hand):
        self._cards = hand.cards
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index < len(self._cards):
            output = self._cards[self._index]
            self._index += 1
            return output
        else:
            raise StopIteration


class Hand:
    def __init__(self) -> None:
        self._cards = []
        self._aces_to_adjust = 0
        self.total = 0

    def __iter__(self):
        return HandIter(self)

    def __len__(self):
        return len(self._cards)

    def __str__(self) -> str:
        if len(self) > 0:
            return ", ".join([str(card) for card in self._cards])
        else:
            return ""

    def add(self, card: Card) -> None:
        self._cards.append(card)
        if card.rank == "Ace":
            self.total += RANKS[card.rank]["max"]
            self._aces_to_adjust += 1
        else:
            self.total += RANKS[card.rank]

    def adjust_for_aces(self) -> int:
        """
        Adjusts the value of the aces to unbust the hand's owner

        Returns
        - Quantity of aces adjusted
        """

        adjusted = 0
        while self._aces_to_adjust > 0 and self.total > 21:
            self._aces_to_adjust -= 1
            adjusted += 1
            self.total -= RANKS["Ace"]["max"]
            self.total += RANKS["Ace"]["min"]
        return adjusted
