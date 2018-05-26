# -*- coding: utf-8 -*-
"""
Simple pythonn program to play the card game of war.

Created on Sat Jan 14 12:19:37 2017

@author: dd
"""
import numpy as np
import matplotlib.pyplot as plt

# - - - - - - -


def shuffle(some_list):
    shuffled_list = []
    for item in some_list:
        iwhere = np.random.choice(range(0, 1 + len(shuffled_list)))
        shuffled_list.insert(iwhere, item)
    return shuffled_list
# - - - - - - -

# lists for the cards
#   'player' are current cards and
#   'pile' are the won cards

player1 = []
pile1 = []
player2 = []
pile2 = []

# create a full deck as tuples: (number, suit)
deck = []
suits = ['S', 'H', 'D', 'C']
for s in suits:
    for icard in range(1, 14):
        card = (icard, s)
        deck.append(card)

# shuffle the deck, twice ;-)
deck = shuffle(shuffle(deck))
print('\n Shuffled Deck :')
print(deck)
print(15 * ' ==' + '\n')

# deal the cards
for icard in range(0, len(deck), 2):
    player1.append(deck[icard])
    player2.append(deck[icard + 1])

print(' Players dealt cards:')
print(player1)
print(15 * ' --')
print(player2)
print(15 * ' ==' + '\n')

nplays = 0
nwars = 0
win_pile = []

# fill these to make a plot
plt_plays = [0]
plt_cards1 = [len(player1)]

# keep playing as long as both players have cards
while (len(player1) + len(pile1) != 0) and (len(player2) + len(pile2) != 0):

    # take a card from the top (= end of list) of each player's cards
    card1 = player1.pop()
    card2 = player2.pop()
    nplays += 1
    # put these cards in the win_pile
    win_pile.append(card1)
    win_pile.append(card2)

    # is it a war ?
    if card1[0] == card2[0]:
        # if it is a war... add cards to win_pile and continue
        print(3 * ' -- War -- ')
        nwars += 1

        # if a player can, put three *more* cards into the win_pile
        if len(player1) > 2:
            # add next 3 cards to the win_pile
            for iadd in range(0, 3):
                win_pile.append(player1.pop())
        else:
            if len(player1) + len(pile1) > 2:
                # pile adds enough, so use them
                player1 += shuffle(pile1)
                pile1 = []
                print(" *-* Player1 including pile for War *-*")
                for iadd in range(0, 3):
                    win_pile.append(player1.pop())
            else:
                # not enough cards: player loses
                win_pile += player1 + pile1
                player1 = []
                pile1 = []

        # same thing for player 2
        if len(player2) > 2:
            # add next 3 cards to the win_pile
            for iadd in range(0, 3):
                win_pile.append(player2.pop())
        else:
            if len(player2) + len(pile2) > 2:
                # pile adds enough, so use them
                player2 += shuffle(pile2)
                pile2 = []
                print(" *-* Player-2 including pile for War *-*")
                for iadd in range(0, 3):
                    win_pile.append(player2.pop())
            else:
                # not enough cards: player loses
                win_pile += player2 + pile2
                player2 = []
                pile2 = []

    # if not a war...
    else:
        if card1[0] > card2[0]:
            print(str(card1) + ' vs ' + str(card2) + ' : 1 wins ')
            # add cards to 1's pile
            pile1 += win_pile
        else:
            print(str(card1) + ' vs ' + str(card2) + ' : 2 wins ')
            # add cards to 2's set
            pile2 += win_pile
        # empty the win_pile
        win_pile = []
        # and save info for plot
        plt_plays.append(nplays)
        plt_cards1.append(len(player1) + len(pile1))

    # does either player need to replenish their cards from their pile
    if len(player1) == 0:
        if len(pile1) == 0:
            print('\n\n  ***  Player 1 out of cards !  ***')
            plt_plays.append(nplays)
            plt_cards1.append(0)
            break
        else:
            # use the pile as is (in order)
            ##player1 = pile1[0:]
            # better, shuffle the pile cards and use them
            player1 = shuffle(pile1)
            pile1 = []
            print(" - Player1 including pile -")
    if len(player2) == 0:
        if len(pile2) == 0:
            print('\n\n  ***  Player 2 out of cards !  ***')
            plt_plays.append(nplays)
            plt_cards1.append(52)
            break
        else:
            # use the pile as is (in order)
            ##player2 = pile2[0:]
            # better, shuffle the pile cards and use them
            player2 = shuffle(pile2)
            pile2 = []
            print(" - Player2 including pile -")

    if nplays > 499:
        print('')
        break

# Note the case of a player going out during a war
if len(win_pile) > 0:
    print('  (War in progress, ' + str(len(win_pile)) + ' cards on table)')

print('\n Summary info:')
print('Number of plays:', nplays)
print('Number of  Wars:', nwars, '\n')
print(" Player 1 cards:")
print(player1)
print(10 * ' --')
print(pile1)
print("\n Player 2 cards:")
print(player2)
print(10 * ' --')
print(pile2)
print('\n ' + str(len(player1 + pile1 + player2 +
                      pile2 + win_pile)) + ' cards in all.\n')

# - - - - Make a plot - - - -
# Close the previous plot
plt.close()
# open a plot
plt.figure(1, [12, 8], frameon=False)
# setup axes
plt.ylim(0.0, 52.0)
plt.plot([0.0, max(plt_plays)], [26.0, 26.0], 'g--')
plt.xlabel('Play Number')
plt.ylabel('Number of Cards (blue-Player1, red-Player2)')
# show the cards vs play
plt.plot(plt_plays, plt_cards1, 'b')
plt.plot(plt_plays, 52 - np.array(plt_cards1), 'r')

plt.title('Number of Cards vs Time')

plt.show()
