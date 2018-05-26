# coding: utf-8
'''
Memory Game where players look for matches in a grid of 'cards'
Tapping the card turns it over, tap another and if they match
you get to add a point to your total.
'''

from scene import *
# import sound
import random
from math import sqrt  # sin, cos, pi
# A = Action


# - - - - - - -
# grid dimensions (at least one is even)
grid_rows = 4  # max 4
grid_cols = 6  # max 7

# define 'textures' to use
backside_tex = Texture('plf:Ground_DirtCenter_rounded')
# the first (index=0) is gold star used when a pair is found
front_textures = [Texture('plf:Item_Star'),
                  Texture('plf:Enemy_FishBlue'),
                  Texture('plf:Tile_Cactus'),
                  Texture('plf:Enemy_FishPink'),
                  Texture('plf:Enemy_Ladybug'),
                  Texture('plf:Enemy_Frog_move'),
                  Texture('plf:Enemy_Mouse'),
                  Texture('plf:Enemy_Fly'),
                  Texture('plf:Enemy_SlimeBlue'),
                  Texture('plf:Enemy_Snail'),
                  Texture('plf:Enemy_SlimeBlock'),
                  Texture('plf:HudPlayer_yellow'),
                  Texture('plf:Enemy_WormPink'),
                  Texture('plf:Enemy_Bee'),
                  Texture('plf:Enemy_Barnacle')]

# - - - - - - -


def shuffle(some_list):
    shuffled_list = []
    for item in some_list:
        iwhere = random.choice(range(0, 1 + len(shuffled_list)))
        shuffled_list.insert(iwhere, item)
    return shuffled_list

# - - - - - - -


def my_dist_to(self, loc):
    '''
    calc distance from self.position to the xy-tuple loc
    '''
    dist = (self.position[0] - loc[0])**2
    dist += (self.position[1] - loc[1])**2
    return sqrt(dist)


class Card (SpriteNode):

    def __init__(self, loc_x, loc_y, tex_num, *args, **kwargs):
        self.tex_num = tex_num
        self.showing = False
        SpriteNode.__init__(self, backside_tex, *args, **kwargs)
        self.position = (loc_x, loc_y)
        self.anchor_point = (0.5, 0.5)

    def show_card(self, show_it):
        # set the card to show it, or not
        if show_it == True:
            self.texture = front_textures[self.tex_num]
            self.showing = True
        else:
            self.texture = backside_tex
            self.showing = False


class MemGame (Scene):

    def setup(self):
        '''
        do setup once at beginning to set things up
        '''
        self.background_color = '#606060'
        # screen sizes
        max_x = self.size.w
        max_y = self.size.h

        # keep track of number of cards that are not matched
        self.num_left = grid_rows * grid_cols
        self.num_misses = 0

        # create a list of card faces to use
        # start with all available tex's
        texs_to_use = list(range(1, len(front_textures)))
        # from these pick the number needed and put them in as pairs
        tex_pairs = []
        for ipair in range(int(self.num_left / 2)):
            tex_pairs += 2 * [texs_to_use.pop()]
        # and shuffle these, a lot
        tex_pairs = shuffle(shuffle(tex_pairs))
        # print("Shuffled pairs: ", tex_pairs)

        # create the cards, in a list
        self.the_cards = []
        # add them by row and column
        for irow in range(0, grid_rows):
            row_y = max_y * (irow + 0.5) / (grid_rows)
            for icol in range(0, grid_cols):
                col_x = max_x * (icol + 0.5) / (grid_cols)
                this_tex = tex_pairs.pop()
                self.the_cards.append(
                    Card(col_x, row_y, this_tex, parent=self))
        # keep track of the cards that are currently turned over
        self.cards_over = []

    def update(self):
        '''
        This is repeatedly called: update, render, update, render
        Nothing to update generally - this game is touch driven
        '''
        # detect the end of the game
        if self.num_left == 0:
            # wait a little and exit
            self.background_color = '#44b844'
            ui.delay(self.view.close, 1.0)

    def touch_ended(self, touch):
        '''
        this is called whenever a touch ends
        '''
        # are two cards turned over?
        # if so, then either set them to stars or hide them again
        if len(self.cards_over) == 2:
            if self.cards_over[0].tex_num != self.cards_over[1].tex_num:
                self.cards_over[0].show_card(False)
                self.cards_over[1].show_card(False)
                self.cards_over = []
                self.num_misses += 1
            else:
                # change to stars
                # they are still 'showing' so further touches are ignored
                self.cards_over[0].tex_num = 0
                self.cards_over[1].tex_num = 0
                self.cards_over[0].show_card(True)
                self.cards_over[1].show_card(True)
                self.cards_over = []
                # decrease the number left to match
                self.num_left -= 2
            print("Num misses: " + str(self.num_misses))
        else:
            # go through the cards and turn one over if touched
            for this_card in self.the_cards:
                if my_dist_to(this_card, touch.location) < 25:
                    # ignore the touch if the card is showing already
                    if not this_card.showing:
                        # turn it face up
                        this_card.show_card(True)
                        # add this to cards_over list
                        self.cards_over.append(this_card)

        # for debug print this
        # print(str(touch.location) + ' - ' + str(len(self.cards_over)))
        # print(self.num_touches)


if __name__ == '__main__':
    print("Game starting...")
    run(MemGame(), LANDSCAPE)
