"""
"""

import entities


def print_dealer(dealer: entities.Hand) -> None:
    """
    Prints the dealer's hand, including the hidden card

    Parameters
    - dealer: Hand - dealer's hand
    """

    print(f"Dealer's hand: {dealer}, xxxxxxxxxxx")


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
        option = input("Play again? (y/n) ").lower()
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


print(r"   ___ _            _     _            _     ")
print(r"  / __\ | __ _  ___| | __(_) __ _  ___| | __ ")
print(r" /__\// |/ _` |/ __| |/ /| |/ _` |/ __| |/ / ")
print(r"/ \/  \ | (_| | (__|   < | | (_| | (__|   <  ")
print(r"\_____/_|\__,_|\___|_|\_\/ |\__,_|\___|_|\_\ ")
print(r"                       |__/                  ")
print()

chips = 100

while True:
    print("The game has begun!")

    deck = entities.Deck()
    deck.shuffle()
    print("The deck of cards was shuffled")

    dealer_hand = entities.Hand()
    dealer_hand.add( deck.deal() )
    hidden_card = deck.deal()

    player_hand = entities.Hand()
    for _ in range(2):
        player_hand.add( deck.deal() )

    print("The cards were dealt")
    
    print(f"You have {chips} chips")
    bet = input_bet(chips)

    print_dealer(dealer_hand)

    keep_playing = True
    while keep_playing:
        print(f"Your hand: {player_hand}")
        move = input_move()
        if move == "hit":
            hit(deck, player_hand)
            keep_playing = not is_bust(player_hand)
        else:
            keep_playing = False

    if not is_bust(player_hand):
        while dealer_hand.total < 17:
            print_dealer(dealer_hand)
            hit(deck, dealer_hand)
        print(f"The hidden card was {hidden_card}")
        dealer_hand.add(hidden_card)
        print(f"The dealer's final hand is {dealer_hand}")
        adjusted = dealer_hand.adjust_for_aces()
        if adjusted > 0:
            print(f"The hand exceeded 21 and {adjusted} aces has their value adjusted")
        if is_bust(dealer_hand):
            print("The dealer is bust")
            win = True
        else:
            print(f"Dealer's hand: {dealer_hand}")
            print(f"Your hand: {player_hand}")
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

    if not play_again():
        break

print(f"You've finished the game with {chips} chips")
