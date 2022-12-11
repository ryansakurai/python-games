"""
BLACKJACK

Implementation of the game blackjack with a human player and the computer as a dealer

- Only hit and stand moves are allowed
- The player begins with 100 chips
- The dealer hits until 17
"""

import entities
import random


def print_dealer(dealer: entities.Hand, hide_first: bool=True) -> None:
    """
    Prints the dealer's hand

    Parameters
    - dealer: Hand - the dealer to be printed
    - hide_first: bool - if the first card must be hidden (default=True)
    """

    if len(dealer)>0 and hide_first:
        cards = [str(card) for card in dealer]
        cards[0] = "xxxxxxxxxxx"
        print(f"Dealer's hand: {', '.join(cards)}")
    else:
        print(f"Dealer's hand: {dealer}")


def print_player(player: entities.Hand) -> None:
    """
    Prints the player's hand

    Parameters
    - player: Hand - the player to be printed
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


def hit(deck: entities.Deck, hand: entities.Hand, show_ace_message: bool=True) -> None:
    """
    The move "hit" is made by the player

    Parameters
    - deck: Deck - deck from which the card will be removed
    - hand: Hand - player's hand
    - show_ace_message: bool - if a message will be shown when aces have their
                                values adjusted (default=True)
    """

    card = deck.deal()
    hand.add(card)
    print(f"Card withdrawn: {card}")
    adjusted = hand.adjust_for_aces()
    if adjusted > 0 and show_ace_message:
        print(f"The hand exceeded 21 and {adjusted} aces has their value adjusted")


def is_bust(hand: entities.Hand) -> bool:
    """
    Parameters
    - hand: Hand - player's hand

    Returns
    - If the player is bust
    """

    return hand.total > 21


def play_again() -> bool:
    """
    Asks if the player wants to play again

    Returns
    - If the player wants to play again
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
    Verifies which one out of two hands got closer to 21

    Parameters
    - hand1: Hand - first hand
    - hand2: Hand - second hand

    Returns
    - If there was a tie, returns None
    - If there wasn't, returns the hand that got closer
    """

    if not is_bust(hand1) and not is_bust(hand2):
        diff1 = 21 - hand1.total
        diff2 = 21 - hand2.total
        if diff1 < diff2:
            return hand1
        elif diff2 < diff1:
            return hand2


def div(wait: bool=True) -> None:
    """
    Prints the div used in the game

    Parameters
    - wait: bool - if it waits for user input after it (default=True)
    """

    BLACK_SUIT_CHARS = ("♠", "♥", "♦", "♣")
    WHITE_SUIT_CHARS = ("♤", "♡", "♢", "♧")
    output = ""

    for _ in range(35):
        output += random.choice(WHITE_SUIT_CHARS)
        output += random.choice(BLACK_SUIT_CHARS)

    if wait:
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
                hit(deck, dealer_hand, show_ace_message=False)
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


if __name__ == "__main__":
    main()
