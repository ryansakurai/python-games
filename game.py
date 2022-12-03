"""
"""

import entities
import random


def print_dealer(dealer: entities.Hand, hide_first: bool=True) -> None:
    """
    """

    if hide_first:
        cards = tuple(dealer)
        print("Dealer's hand: xxxxxxxxxxx", end="")
        for i in range(1, len(cards)):
            print(f", {cards[i]}", end="")
        print()
    else:
        print(f"Dealer's hand: {dealer}")


def print_player(player: entities.Hand) -> None:
    """
    """

    print(f"Your hand: {player}")


def input_bet(max: int) -> int:
    """
    Reads bet from user and validates it

    Parameters
    - max: int - maximum bet allowed

    Returns
    - The bet read
    """

    while True:
        try:
            bet = int( input("How many chips do you wanna bet? ") )
        except:
            print("Amount must be an integer")
        else:
            if bet > max:
                print("You can't bet more chips that you have!")
            else:
                return bet


def input_move() -> str:
    """
    Reads move from user and validates it

    Returns
    - "hit" or "stand"
    """

    while True:
        move = input("Hit or stand? ").lower()
        if move == "hit" or move == "stand":
            return move
        else:
            print("Invalid input!")


def hit(deck: entities.Deck, hand: entities.Hand):
    """
    """

    card = deck.deal()
    hand.add(card)
    print(f"Card withdrawn: {card}")
    if hand.total > 21:
        adjusted = hand.adjust_for_aces()
        if adjusted > 0:
            print(f"The hand exceeded 21 and {adjusted} aces has their value adjusted")


def is_bust(hand: entities.Hand) -> bool:
    """
    """

    return hand.total > 21


def play_again() -> bool:
    """
    """

    while True:
        option = input("Play again (y/n)? ").lower()
        if option == 'y':
            return True
        elif option == 'n':
            return False
        else:
            print("Invalid option!")


def got_closer(hand1: entities.Hand, hand2: entities.Hand) -> entities.Hand | None:
    """
    """

    if not is_bust(hand1) and not is_bust(hand2):
        diff1 = 21 - hand1.total
        diff2 = 21 - hand2.total
        if diff1 > diff2:
            return hand1
        elif diff2 > diff1:
            return hand2


def div(wait: bool=True) -> None:
    """
    """

    BLACK_SUIT_CHARS = ("♠", "♥", "♦", "♣")
    WHITE_SUIT_CHARS = ("♤", "♡", "♢", "♧")
    output = ""

    for _ in range(25):
        output += random.choice(WHITE_SUIT_CHARS)
        output += random.choice(BLACK_SUIT_CHARS)

    if wait:
        input()
        print(output + "\n")
    else:
        print("\n" + output + "\n")


print(r"   ___ _            _     _            _     ")
print(r"  / __\ | __ _  ___| | __(_) __ _  ___| | __ ")
print(r" /__\// |/ _` |/ __| |/ /| |/ _` |/ __| |/ / ")
print(r"/ \/  \ | (_| | (__|   < | | (_| | (__|   <  ")
print(r"\_____/_|\__,_|\___|_|\_\/ |\__,_|\___|_|\_\ ")
print(r"                       |__/                  ")
print()

chips = 100

while True:
    print("The round has begun!")

    deck = entities.Deck()
    deck.shuffle()
    print("The deck of cards was shuffled")

    dealer_hand = entities.Hand()
    player_hand = entities.Hand()
    for _ in range(2):
        player_hand.add( deck.deal() )
        dealer_hand.add( deck.deal() )

    print("The cards were dealt")
    
    print(f"You have {chips} chips")
    bet = input_bet(chips)

    div(wait=False)
    print("Your turn")
    div(wait=False)

    keep_playing = True
    while keep_playing:
        print_dealer(dealer_hand)
        print_player(player_hand)
        move = input_move()
        if move == "hit":
            hit(deck, player_hand)
            keep_playing = not is_bust(player_hand)
        else:
            keep_playing = False
        div(wait=False)

    if not is_bust(player_hand):
        print("Dealer's turn")
        div(wait=False)

        while dealer_hand.total < 17:
            print_dealer(dealer_hand)
            hit(deck, dealer_hand)
            div()
        print(f"The hidden card was {tuple(dealer_hand)[0]}")
        print(f"The dealer's final hand is {dealer_hand}")

        div()

        print(f"Dealer's hand: {dealer_hand}")
        print(f"Your hand: {player_hand}")
        if is_bust(dealer_hand):
            print("The dealer is bust")
            win = True
        else:
            winner = got_closer(dealer_hand, player_hand)
            if winner == player_hand:
                win = True
            elif winner == dealer_hand:
                win = False
            else:
                win = None
    else:
        print("You're bust!")
        win = False

    if win == True:
        chips += bet
        print(f"You win! (+{bet} chips)")
    elif win == False:
        chips -= bet
        print(f"You lose! (-{bet} chips)")
    else:
        print("There was a tie")
    print(f"You now have {chips} chips")

    if chips <= 0:
        print("You are out of chips, the game is over")
        break
    elif not play_again():
        break

    div(wait=False)

print(f"You've finished the game with {chips} chips")
