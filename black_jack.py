#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import random
import pyfiglet
import colorama
import time


# In[2]:


#ranks = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King')
ranks = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K')
#suits = ('Spade', 'Clover', 'Diamond', 'Heart')
suits = ('S', 'C', 'D', 'H')
#values = {'1':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10, 'Jack':10, 'Queen':10, 'King':10}
values = {
    '1': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    '10': 10,
    'J': 10,
    'Q': 10,
    'K': 10}


# In[3]:


def highscores():
    pass


# In[4]:


class game_help():

    ''' Rules : Dealer hits hard 17.
        if player wins with blackjack : 3:2 i.e if bet 1 will get 1.5 , total 2.5
        if player wins  : 1:1 , if bet 1 will get 1, total 2
        if player draws : bet returned. If bet 1 , will get nothing. total 1
        if player loses : bet lost, if bet 1, total 0
        if player surrenders : 2:1 , if bet 1 will get 0.5 back . total 0.5
        if player doubles down:
        if player splits:
        if player insures:
    '''
    print('\n' * 100)
    print(
        pyfiglet.figlet_format(
            "Blackjack",
            font='slant',
            width=100,
            justify='center'))


# In[5]:


def card_graph(cards, hidden=None):

    colorama.init(autoreset=True)
    card_len = len(cards)

    if hidden is not None:

        print(f'::::::::::\t' * 2, end='')
        print('')
        print(f'::      ::\t', end='')
        print(f'::     {cards[1].suit}::')
        print(f'::      ::\t' * 2, end='')
        print('')
        print(f'::HIDDEN::\t', end='')
        rank = cards[1].rank.rjust(2, ' ')
        print(f'::  {rank}  ::\t', end='')
        print('')
        print(f'::      ::\t' * 2, end='')
        print('')
        print(f'::      ::\t', end='')
        print(f'::     {cards[1].suit}::')
        print(f'::::::::::\t' * 2, end='')
        print('')

    else:
        print(f'::::::::::\t' * card_len, end='')
        print('')
        for i in range(0, card_len):
            print(f'::     {cards[i].suit}::\t', end='')
        print('')
        print(f'::      ::\t' * card_len, end='')
        print('')
        for i in range(0, card_len):
            rank = cards[i].rank.rjust(2, ' ')
            print(f'::  {rank}  ::\t', end='')
        print('')
        print(f'::      ::\t' * card_len, end='')
        print('')
        for i in range(0, card_len):
            print(f'::     {cards[i].suit}::\t', end='')
        print('')
        print(f'::::::::::\t' * card_len, end='')
        print('')


# In[6]:


class Player():

    ''' This class is to create a player. '''
    count = 0

    def __init__(self, name):
        self.name = name
        self.bank = 1000
        #self.final_result = None
        self.blackjack = None

        Player.count += 1
        self.id = Player.count

        self.bet = 0  # start bet is zero when player created.
        print(f'Player created.\nName : {self.name} \nBalance : ${self.bank}')

        self.value = 0  # value at start is zero
        self.cards = list()

    @staticmethod
    def get_name():
        ''' This function is to get name of the player. '''
        while True:
            try:
                name = str(input('Enter player\'s name :  '))
                if name in {''}:
                    raise ValueError
            except ValueError:
                print(f'Do not enter blank name.')
            else:
                break
        return name

    @staticmethod
    def get_bank(name):
        ''' This function is to get the purse value of the player. '''
        while True:
            try:
                bank = int(input(f'Hello {name}! Enter your purse value : $'))
                if bank < 100:
                    raise ValueError
            except ValueError:
                print(f'Purse value cannot be less than $100 / alphabets / blank.')
            else:
                break

        return bank

    def get_bet(self):
        ''' This function is to get the amount of bet player want's to set '''
        while True:
            try:
                self.bet = int(
                    input(f'Hello {self.name}! How much would you like to bet : $'))
                if self.bet > self.bank or self.bet < 10:
                    raise ValueError
            except ValueError:
                print(f'Bet value cannot be less than $10 or greater than the balance.')
            else:
                break

        ### Subtract the bet amount from the balance of the player ###
        self.bank -= self.bet
        print(
            f'Bet placed for ${self.bet} by {self.name}. New balance : ${self.bank}')

    def set_value(self, special=None):

        card_sum = sum([card.card_value() for card in self.cards])

        if '1' in [card.rank for card in self.cards] and card_sum == 11:
            # Ace present check for blackjack condition , Note cards are objects
            # If ace is considered as 11, value will be 11 + 10
            self.value = 21
        elif '1' in [card.rank for card in self.cards] and special:
            max_value = max(card_sum, card_sum + 10)
            if max_value <= 21:
                self.value = max_value
        else:
            self.value = sum([card.card_value() for card in self.cards])

    def display(self):

        print(f'     {self.name.upper()}\'s CARDS :')
        card_graph(self.cards)
        print(f'{self.name} cards value : {self.value}')
        print('\n')

    def cards_clear(self):
        ''' This function is to clear cards and value on replay'''
        self.cards.clear()
        self.value = 0
        self.blackjack = None

    def black_win_bet(self):
        self.bank += (self.bet * 2.5)    # Bet + 3/2 bet

    def win_bet(self):
        self.bank += (self.bet * 2)      # Bet + 1/1 bet

    def lose_bet(self):
        self.bank = self.bank

    def tie_bet(self):
        self.bank += self.bet


# In[7]:


class Dealer():

    ''' This class is to create a dealer and store his info. '''

    def __init__(self):
        self.value = 0
        self.cards = list()
        self.name = 'Dealer'
        self.blackjack = None

    def set_value(self):

        card_sum = sum([card.card_value() for card in self.cards])

        if '1' in [card.rank for card in self.cards] and card_sum == 11:
            # Ace present check for blackjack condition , Note cards are objects
            # If ace is considered as 11, value will be 11 + 10
            self.value = 21
        else:
            self.value = sum([card.card_value() for card in self.cards])

        ### NOTE : Regarding dealer and ace. ###
        '''
        When players ask dealer to stand :

        A hand with an ace which sums to 17 is called soft 17.
        Casinos differ on whether dealer hits or stands after getting to soft 17.
        It is to casinos advantage if dealer keeps hitting even with soft 17.

        Our dealer also hits even though he has soft 17.

        '''

    def display(self, hidden=None):

        print(f'     DEALERS\'s CARDS :')
        card_graph(self.cards, hidden)
        if hidden is None:
            print(f'Dealer\'s cards value : {self.value}')
        print('\n')

    def cards_clear(self):
        ''' This function is to clear cards and value on replay'''
        self.cards.clear()
        self.value = 0
        self.blackjack = None


# In[8]:


class Card():

    ''' This class is to create a card instance using suit and rank. '''

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def card_value(self):
        return values[self.rank]


# In[9]:


class Deck():

    ''' This class is to create a deck of cards. '''

    def __init__(self):
        self.deck = list()
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))  # 52 card objects created
        random.shuffle(self.deck)
        print(f'Deck created and shuffled.')

    def shuffle(self):
        ''' This function is used to shuffle the deck. '''
        random.shuffle(self.deck)

    def draw(self):
        ''' This function is to draw initial card from the deck. Gamer is either players or dealer object. '''
        return self.deck.pop(), self.deck.pop()  # pop two cards from the deck list and return
        # print(len(self.deck))                      #lenght for debug

    def hit(self):

        return self.deck.pop()   # Pop card from the deck objects deck


# # 1 player 1 dealer scenario basic
# 1. first players chance
# 2. if player stands then only dealer chance
# 3. ace condition - done
# 4. better display : show better cards, display dealers cards
# 5. dealer has no option to draw until his count crosses 17 [ ace is valued accordingly ] - done
# 6. store purse for replay.
# 7. ace conition of dealer at first draw : needs to let player play or insure.
# 8. add create py file in ipynb - done
# 9. better replay looping
# 10. store high score
# 11. display final score
# 12. PENDING : New info : Only if the first draw hits 21 its called blackjack. And blackjacks trounce even if multiple card values are summed to 21
#
# ### future ###
# 1. insurance
# 2. split
# 3. double down
# 4. multiplayer
# 5. multideck
# 6. pygame  : In future, display game using pygame library.
#
# ### BUG ###
# after hitting and standing. even if values are same. player loses. check
#
#
# ### cases ###
# ## case 1 ##
# player gets black jack on first try.
# check dealers
# if same WINCHECK -> PUSH
# elif
#
# ## case 2 ##
# player gets cards and chooses to hit.
# # sub-case 1#
# value goes over 21 [adusting ace]  WINCHECK -> BUST
# # sub-case 2#
# user hits blackjack WINCHECK -> goto case 1
# # sub-case 3#
# user chooses to stand WINCHECK -> goto case 3
#
# ## case 3 ##
# player gets cards and chooses to stand.
# dealer reveals cards.
# # sub-case 1#
# dealer hits blackjack WINCHECK -> LOSE
# # sub-case 2#
# dealer goes over 21 WINCHECK -> WIN
# # sub-case 3#
# dealer goes over 17 WINCHECK -> compare values of cards -> WINCHECK -> WIN OR LOSE
#
#

# In[10]:


def graffiti(result):

    print('\n')
    print(
        pyfiglet.figlet_format(
            result.upper(),
            font='slant',
            width=100,
            justify='center'))
    print('\n')


# In[11]:


def printing(player, dealer, result):
    '''

    blackjack cases
    case 0 : both blackjack                   - done
    case 1 : player black jack                - done
    case 2 : dealer black jack                - done
    case 3 : player busts                     - done
    case 4 : player hits 21, dealer blackjack - done
    case 5 : dealer busts                     - done
    comparison:
    case 6 : player hits 21 and dealer hist 21 - done
    case 7 : player hits 21 , dealer less      - done
    case 8 : player higher, dealer less        - done
    case 9 : dealer high, player less          - done
    case 10 : player and dealer value same     - done

    '''

    if result == 0:
        print('\n\n')
        print(f'{player.name} hits BLACKJACK !')
        print('Checking dealer\'s cards.....   ', end='')
        print(f'Dealer hits BLACKJACK as well !')
        print(f'{player.name} and dealer PUSH ! Game tie !')
        graffiti('push')
    elif result == 1:
        print('\n\n')
        print(f'{player.name} hits BLACKJACK ! {player.name} WINS ! Congratulations !')
        graffiti('win')
    elif result == 2:
        print('\n\n')
        print(f'Dealer\'s hit BLACKJACK ! {player.name} LOST !')
        graffiti('lost')
    elif result == 3:
        print('\n\n')
        print(f' {player.name} BUST ! {player.name} LOST !')
        graffiti('lost')
    elif result == 4:
        print('\n\n')
        print(f'Dealer\'s hit BLACKJACK ! {player.name} LOST !')
        graffiti('lost')
    elif result == 5:
        print('\n\n')
        print(f' Dealer BUST ! {player.name} WINS !')
        graffiti('win')
    elif result == 6 or result == 10:
        print('\n\n')
        print(f'{player.name} and dealer PUSH ! Game tie !')
        graffiti('push')
    elif result == 7 or result == 8:
        print('\n\n')
        print(
            f'{player.name} WINS ! {player.name}\'s cards have greater value ! Congratulations !')
        graffiti('win')
    elif result == 9:
        print('\n\n')
        print(f'{player.name} LOST ! Dealer\'s cards have greater value !')
        graffiti('lost')


# In[12]:


def blackjack_check(dealer, player):

    if player.value == 21 and dealer.value == 21:
        return 0
    elif player.value == 21:
        return 1
    elif dealer.value == 21:
        return 2
    else:
        return 100


# In[13]:


def top_check(dealer, player):

    if player.value == 21 and dealer.blackjack:
        return 4
    elif player.value == 21:
        return 100  # not complete result , needs to stand


# In[14]:


def bust_check(dealer=None, player=None):

    if dealer is not None:
        if dealer.value > 21:
            return 5
    elif player is not None:
        if player.value > 21:
            return 3

    return 101


# In[15]:


def win_check(dealer, player):

    if player.value == 21 and dealer.value == 21:
        return 6
    elif player.value == 21 and dealer.value < 21:
        return 7
    elif dealer.value < player.value:
        return 8
    elif dealer.value > player.value:
        return 9
    elif dealer.value == player.value:
        return 10
    else:
        return 102         # impossible result, just to break while loop

    # This push is a tie, Not a blackjack push


# In[16]:


def hit_or_stand(player):

    hors = str(input(f'{player.name}, Do you want to hit or stand ? [H/S] :'))
    while hors.lower() not in {'h', 's', 'hit', 'stand'}:
        hors = str(input(f'{player.name}, Enter hit or stand only ? [H/S] :'))
    return hors.lower()


# In[17]:


def game(replay=None, players=None, dealer=None):
    ''' This function is to conduct the game. '''

    ### highscores ###
    #highscores = []
    # if os.path.exists('HIGHSCORES.txt'):
    #    with open('HIGHSCORES.txt','r') as highscore:
    #        for i in range(0,5):
    #            highscores[i] = highscore.readline()
    # else:
    #    with open('HIGHSCORES.txt','w') as highscore:
    #        print('')

    ### Create players for the game ###
    if replay is None:
        players = list()   # For supporting multiplayer in future

        name = Player.get_name()
        # Player created and appended to playes list
        players.append(Player(name))

        ### Create a dealer for the game ###
        dealer = Dealer()

    else:
        # If replay remember players name and balance, but remove cards from
        # dealer and player
        players = players
        for player in players:
            player.cards_clear()
        dealer.cards_clear()

    ### Setup deck ###
    play_deck = Deck()
    print([(x.suit, x.rank) for x in play_deck.deck])  # print deck for debug

    ### Bet amount ###
    player1 = players[0]  # Since currently single player game
    player1.get_bet()

    ### Draw the cards for dealer and players ###
    # for card in play_deck.draw(dealer):
    for card in play_deck.draw():
        dealer.cards.append(card)
    dealer.set_value()
    # print(f'Initial dealer value {dealer.value}') # debug

    for card in play_deck.draw():
        player1.cards.append(card)
    player1.set_value()
    # print(f'Initial player value : {player1.value}')   # debug

    ### Display cards and values ###
    print('\n\n' * 100)
    dealer.display(hidden='x')
    player1.display()

    ##### Concept of insurance ##########
    ### Initial check : Only black jack ####
    check = blackjack_check(dealer, player1)

    if check == 0:
        player1.blackjack = dealer.blackjack = True
    elif check == 1:
        player1.blackjack = True
        dealer.blackjack = False
    elif check == 2:
        dealer.blackjack = True
        player1.blackjack = False

    if check in {
            0, 1}:  # if only player has a blackjack or both have ### end game
        time.sleep(2)
        print('\n' * 100)
        dealer.display()
        player1.display()
        player1.blackjack = True
        if check == 0:
            dealer.blackjack = True
        printing(player1, dealer, check)
    else:
        hors = None
        while True:
            if hors != 'as':
                hors = hit_or_stand(player1)

            if hors in {'h', 'hit'}:

                # player1.cards is a list, an atribute of player1 object
                player1.cards.append(play_deck.hit())
                player1.set_value()
                print([(x.rank, x.suit) for x in player1.cards])  # debug
                print(player1.value)  # debug

                dealer.display(hidden='x')
                player1.display()

                # check if player1 is bust # check will be 3 if player busts
                check = bust_check(player=player1)
                if check == 3:
                    break

                check = top_check(dealer, player1)
                if check == 4:                          # player hits 21 and dealer hits blackjack
                    break
                elif check == 100:                      # player hits 21 , needs to auto stand.
                    hors = 'as'

            elif hors in {'s', 'stand', 'as'}:

                if dealer.blackjack:
                    check = 2                           # dealer blackjack restore
                    dealer.display()
                    player.display()
                    break

                ### Special ace case ###
                ## If player has ace in his cards, sum of cmp(soft,hard) must be taken ##
                # EX : player 1,7  dealer 7,9
                player1.set_value(special=True)

                while dealer.value < 17:
                    dealer.cards.append(play_deck.hit())
                    dealer.set_value()
                    print(dealer.value)  # debug
                    print(player1.value)  # debug
                    print('\n' * 50)
                    dealer.display()
                    player1.display()
                    time.sleep(2)

                print('\n' * 50)
                dealer.display()
                player1.display()
                time.sleep(2)

                # check if dealer is bust
                check = bust_check(dealer=dealer)
                if check == 5:
                    break

                check = win_check(dealer, player1)
                print(f'last check : {check}')
                if check != 102:
                    break

        printing(player1, dealer, check)

    ### Bank update ###
    if check in {0, 6, 10}:
        player1.tie_bet()
    elif check in {2, 3, 4, 9}:
        player1.lose_bet()
    elif check in {5, 7, 8}:
        player1.win_bet()
    else:
        player1.black_win_bet()

    return players, dealer      # for replay


# In[18]:


def main():
    ''' This function controls everything '''

    ### Welcome ###
    print('Welcome to BLACKJACK.')
    print('\n')
    # game_help()

    ### Start ###
    while True:

        print('Are you ready to play the game ? : [Y/N] ')
        try:
            start = str(input()).lower()
            if start not in {'y', 'n', 'yes', 'no'}:
                raise ValueError
        except ValueError:
            print('Enter either Y or N.')
        else:
            if start in {'y', 'Y'}:
                print('\n\n' * 100)
                players, dealer = game()

                #### If bank goes below 10 should not allow to play ###
                player1 = players[0]
                if player1.bank <= 10:
                    print('Bank balance is below the minimum of $10 required')
                else:

                    while True:  # Replay Loop ### TRY CATCH rmaining ###

                        print('\n')
                        print(
                            f'Player score : \nName : {player1.name} \nBalance : ${player1.bank}')
                        print('\n')
                        replay = str(
                            input('Play once again ? : [Y/N] ')).lower()
                        if replay in {'y', 'yes'}:
                            players, dealer = game(
                                replay=replay, players=players, dealer=dealer)
                        else:
                            start = 'n'
                            print('\n')
                            print(
                                f'Final score : \nName : {player1.name} \nBalance : ${player1.bank}')
                            print('\n')

                            # with open('HIGHSCORES.txt','w') as highscore:
                            #    for i in highscores:
                            #        highscore.writeline(i)

                            break

            else:
                print('Bye. Have a nice day !!!')
            break


# In[ ]:

try:
    terminal = get_ipython().__class__.__name__
except Exception:
    pass
else:
    if get_ipython().__class__.__name__ == 'ZMQInteractiveShell':
        get_ipython().system('jupyter nbconvert --to python black_jack.ipynb')
        get_ipython().system('pylint black_jack.py')
        get_ipython().system('autopep8 --in-place --aggressive black_jack.py')
        get_ipython().system('pylint black_jack.py  ')
finally:
    if __name__ == "__main__":
        main()
