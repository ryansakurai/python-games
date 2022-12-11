"""
BLACKJACK

Implementation of the game blackjack with a human player and the computer as a dealer

- Only hit and stand moves are allowed
- The player begins with 100 chips
- The dealer hits until 17
"""

import entities
import random


def print_dealer_hand(hand: entities.Hand, hide_first_card: bool=True) -> None:
    if len(hand)>0 and hide_first_card:
        cards = [str(card) for card in hand]
        cards[0] = "xxxxxxxxxxx"
        print(f"Dealer's hand: {', '.join(cards)}")
    else:
        print(f"Dealer's hand: {hand}")


def print_player_hand(player: entities.Hand) -> None:
    print(f"Your hand: {player}")


def input_bet(max_bet: int) -> int:
    while True:
        try:
            bet = int( input("How many chips do you wanna bet? ") )
        except:
            print("Amount must be an integer")
        else:
            if bet > max_bet:
                print("You can't bet more chips that you have!")
            else:
                return bet


def input_move() -> str:
    """
    Returns
    - "hit" or "stand"
    """

    while True:
        move = input("Hit or stand? ").lower()
        if move == "hit" or move == "stand":
            return move
        else:
            print("Invalid input!")


def hit(deck: entities.Deck, hand: entities.Hand, show_ace_message: bool=True) -> None:
    """
    Parameters
    - show_ace_message - if a message will be shown when aces have their
                        values adjusted
    """

    card = deck.deal()
    hand.add(card)
    print(f"Card withdrawn: {card}")
    adjusted = hand.adjust_for_aces()
    if adjusted > 0 and show_ace_message:
        print(f"The hand exceeded 21 and {adjusted} aces has their value adjusted")


def is_bust(hand: entities.Hand) -> bool:
    return hand.total > 21


def play_again() -> bool:
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
    Returns
    - The hand that got closer
    - None, if none got closer
    """

    if not is_bust(hand1) and not is_bust(hand2):
        diff1 = 21 - hand1.total
        diff2 = 21 - hand2.total
        if diff1 < diff2:
            return hand1
        elif diff2 < diff1:
            return hand2


def print_div(sleep: bool=True) -> None:
    BLACK_SUIT_CHARS = ("♠", "♥", "♦", "♣")
    WHITE_SUIT_CHARS = ("♤", "♡", "♢", "♧")
    output = ""

    for _ in range(35):
        output += random.choice(WHITE_SUIT_CHARS)
        output += random.choice(BLACK_SUIT_CHARS)

    if sleep:
        input()
        print(output + "\n")
    else:
        print("\n" + output + "\n")


def main():
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

        dealer_hand.adjust_for_aces()
        adjusted = player_hand.adjust_for_aces()
        if adjusted > 0:
            print(f"Your hand exceeded 21 and {adjusted} aces has their value adjusted")
        
        print(f"You have {chips} chips")
        bet = input_bet(chips)

        print_div(sleep=False)
        print("Your turn")
        print_div(sleep=False)

        keep_playing = True
        while keep_playing:
            print_dealer_hand(dealer_hand)
            print_player_hand(player_hand)
            move = input_move()
            if move == "hit":
                hit(deck, player_hand)
                keep_playing = not is_bust(player_hand)
            else:
                keep_playing = False
            print_div(sleep=False)

        if not is_bust(player_hand):
            print("Dealer's turn")
            print_div(sleep=False)

            while dealer_hand.total < 17:
                print_dealer_hand(dealer_hand)
                hit(deck, dealer_hand, show_ace_message=False)
                print_div()
            print(f"The hidden card was {tuple(dealer_hand)[0]}")
            print(f"The dealer's final hand is {dealer_hand}")

            print_div()

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

        print_div(sleep=False)

    print(f"You've finished the game with {chips} chips")


if __name__ == "__main__":
    main()
