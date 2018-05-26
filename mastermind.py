#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MasterMind game program

Created on Fri Jun 16 17:35:00 2017
Updated w/bug fix 6/17/17
@author: dd
"""
import random

Colors = ['Red', 'Yel', 'Grn', 'Blu', 'Blk', 'Wht']
Ncolors = len(Colors)
Nholes = 4


def all_codes():
    # create a list of lists each with single color
    out = list()
    for clr in Colors:
        out.append([clr])
    # create bigger list (more) by adding in turn each color to the
    # current list (out). Do this Nholes-1 times:
    for indholes in range(Nholes - 1):
        more = list()
        for ind in range(len(out)):
            for indclr in range(Ncolors):
                more.append(out[ind] + [Colors[indclr]])
        out = more
    return out


def check_codes(in1, in2):
    """
    Compare the two codes and return result as
    10*<num-right-place-right-color> + <num-right-color>

    >>> code1 = [1,2,3,4]
    >>> code2 = [2,1,3,1]
    >>> print(check_codes(code1,code2))
    12

    >>> code1 = [1,2,3,4]
    >>> code2 = [2,2,2,2]
    >>> print(check_codes(code1,code2))
    10

    >>> code1 = [3,3,3,3]
    >>> code2 = [1,2,3,4]
    >>> print(check_codes(code1,code2))
    10

    """
    # don't modify the input lists
    code1 = list(in1)
    code2 = list(in2)
    black = 0
    white = 0
    # first, look for exact matches
    for ind1 in range(len(code1)):
        if code1[ind1] == code2[ind1]:
            # got a "black" match
            black += 1
            # mark these two as used already
            code1[ind1] = 'used'
            code2[ind1] = 'used'
    # now go through again picking a match anywhere
    for ind1 in range(len(code1)):
        if code1[ind1] != 'used':
            for ind2 in range(len(code2)):
                # check for color match with other position
                if code1[ind1] == code2[ind2]:
                    # got a "white" match
                    white += 1
                    code2[ind2] = 'used'
                    break  # out of the 'for ind2' loop
    return 10 * black + white


def prune_possible(poss_codes, guess_code, score):
    """
    Go through the possible codes and score them compared to
    the guess code, keep only the ones that give the score value.
    """
    out_codes = list()
    for ind in range(len(poss_codes)):
        if check_codes(poss_codes[ind], guess_code) == score:
            out_codes.append(poss_codes[ind])
    return out_codes


def play_game():
    print("")
    print('    Starting MasterMind !')
    possible_codes = all_codes()
    print('Number possible codes = ', len(possible_codes))
    print("")
    print("Enter score as:")
    print("  10*black# + white#, e.g. 21")
    print("")
    # print(possible_codes)
    num_guesses = 0
    # Select a guess from the possible codes:
    my_guess = random.choice(possible_codes)
    num_guesses += 1
    print("My starting guess : ")
    print(" ", my_guess)
    my_score = int(input("  What's the score? "))
    # loop until it's figured out
    while my_score != 40:
        print("OK, ...thinking...")
        # remove not possible codes
        possible_codes = prune_possible(possible_codes, my_guess, my_score)
        # catch the case of nothing possible...
        if len(possible_codes) == 0:
            print("")
            print(" *** Hey, wait a minute! ***")
            print(" Something doesn't compute! :-(")
            return
        print("         ...narrowed to ", len(possible_codes))
        print("")
        if len(possible_codes) < 10:
            for code in possible_codes:
                print(code)
            print("")
        my_guess = random.choice(possible_codes)
        num_guesses += 1
        print("I'll try : ")
        print(" ", my_guess)
        my_score = int(input("  What's the score? "))
    # got em ;-)
    print("")
    print("   Hah!  Got'em!  (in " + str(num_guesses) + " guesses)")
    return

if __name__ == "__main__":
    play_game()
