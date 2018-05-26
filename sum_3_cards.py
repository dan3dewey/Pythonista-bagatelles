# sum_cards.py
# Makes a histogram of the sum of three cards from a deck;
# 10 sets of 3 are taken from each shuffling of a deck.

# run it at os command line:
# osprompt> py sum_3_cards.py

import random
import matplotlib.pyplot as plt

# zeroed histogram to start, 41 bins indexed from 0 to 40
histo = 41 * [0]

# Do a number of shuffles
for nshuffle in range(15000):
    # Numbers 0 to 51 are a deck of cards...
    # shuffle deck of cards and choose the first 30 of them
    cards = random.sample(range(52), 30)
    # print(cards)
    # replace them with their numerical value (A=1, ..., K=13), ignoring suit
    for i in range(len(cards)):
        cards[i] = (cards[i] % 13) + 1
    # print(cards)
    # form the sums of each three in a row
    sums = []
    for istart in range(10):
        sums.append(sum(cards[3 * istart:3 * istart + 3]))
    # print(sums)
    # add these to the histogram
    for i in sums:
        histo[i] += 1

print()
print(histo)

# plot bins 2 to 40 (bins 2 and 40 will be zero valued)
plt.step(range(2, len(histo)), histo[2:], where='mid')
plt.show()
