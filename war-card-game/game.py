"""
WAR CARD GAME

Simulation of the card game war that gives stats at the end of the match.

- All 52 cards are used
- The cards are shuffled only once, at the start of the match
- When war happens, each player withdraws 3 cards
"""

from typing import Iterable, Tuple
import entities


def deal_cards(cards: entities.FullDeck, player1: entities.Player, player2: entities.Player) -> None:
    while len(cards) > 0:
        for player in (player1, player2):
            card = cards.remove_card()
            player.add_cards(card)


def gather_cards_to_war(cards_gathered: Iterable[entities.Card], player1: entities.Player, player2: entities.Player, amount: int) -> Tuple[entities.Card]:
    """
    Returns
        All the cards gathered or None, if not possible
    """

    cards_gathered = list(cards_gathered)
    for player in (player1, player2):
        try:
            for _ in range(amount):
                cards_gathered.append( player.remove_card() )
        except IndexError:
            return None
    return cards_gathered


def find_loser(player1: entities.Player, player2: entities.Player) -> entities.Player | None:
    """
    Returns
    The loser or None, if there isn't one yet
    """

    for player in (player1, player2):
        if len(player) <= 0:
            return player

def print_result(player1: entities.Player, player2: entities.Player, qt_rounds: int, qt_wars: int) -> None:
    if find_loser(player1, player2) == player1:
        print(f"{player2.name} has won the game!")
    else:
        print(f"{player1.name} has won the game!")
    print(f"Number of rounds: {qt_rounds}")
    print(f"Number of wars: {qt_wars}")
    print()
    print(player1)
    print(player2)


def main():
    print(r":::       :::     :::     :::::::::  ")
    print(r":+:       :+:   :+: :+:   :+:    :+: ")
    print(r"+:+       +:+  +:+   +:+  +:+    +:+ ")
    print(r"+#+  +:+  +#+ +#++:++#++: +#++:++#:  ")
    print(r"+#+ +#+#+ +#+ +#+     +#+ +#+    +#+ ")
    print(r" #+#+# #+#+#  #+#     #+# #+#    #+# ")
    print(r"  ###   ###   ###     ### ###    ### ")
    print()

    WAR_QT_CARDS = 3
    player1 = entities.Player("Player 1")
    player2 = entities.Player("Player 2")
    full_deck = entities.FullDeck()
    full_deck.shuffle()
    deal_cards(full_deck, player1, player2)
    cards_in_table = []
    rounds = 0
    wars = 0

    while True:
        rounds += 1

        ## moves
        card1 = player1.remove_card()
        cards_in_table.append(card1)
        card2 = player2.remove_card()
        cards_in_table.append(card2)

        ## comparing
        if entities.compare(card1, card2) > 0:
            player1.add_cards(cards_in_table)
            player1.win_round()
            cards_in_table.clear()
        elif entities.compare(card1, card2) < 0:
            player2.add_cards(cards_in_table)
            player2.win_round()
            cards_in_table.clear()
        else:
            wars += 1
            cards_in_table = gather_cards_to_war(cards_in_table, player1, player2, WAR_QT_CARDS)

        if find_loser(player1, player2) != None:
            break

    print_result(player1, player2, rounds, wars)


if __name__ == "__main__":
    main()
