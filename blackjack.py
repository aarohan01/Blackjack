#!/usr/bin/env python
# coding: utf-8

# # Future releases:
# 1. Better highscore handling by using csv or pandas - done
# 2. Better replay looping, code optimization
# 3. Use pygame for displaying game
# 4. Nano editor like options for hit stand
# 5. Better clear screen - done
# 6. Add colors - done
# 7. Add better fonts for cards as well as text.
#
# ### gameplay :
# 0. surrender - done
# 1. insurance
# 2. split
# 3. double down
# 4. multiplayer
# 5. multideck
#
#

# In[5]:


import os                     # To clear screen and check file
import random                 # Random selection
import pyfiglet               # Graffiti and ascii art
import time                   # Sleep
import pandas as pd           # Highscores csv
from termcolor import colored  # Colour
from colorama import init     # Used to initiate teminal for color


# In[3]:


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
space = '\t\t\t\t '
spacec = '\t\t'  # for cards


# In[ ]:


def clearscreen():
    ''' This function is to clear screen. '''
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


# In[8]:


class game_help():

    '''
        This function is to display logo as well as help. Help is yet to be configured.
        Rules : Dealer hits hard 17.
        if player wins with blackjack : 3:2 i.e if bet 1 will get 1.5 , total 2.5
        if player wins  : 1:1 , if bet 1 will get 1, total 2
        if player draws : bet returned. If bet 1 , will get nothing. total 1
        if player loses : bet lost, if bet 1, total 0
        if player surrenders : 2:1 , if bet 1 will get 0.5 back . total 0.5
        if player doubles down:
        if player splits:
        if player insures:
    '''
    # print('\n'*100)
    clearscreen()
    print('\n' * 3)
    print(
        pyfiglet.figlet_format(
            "Blackjack",
            font='slant',
            width=100,
            justify='center'))


# In[4]:


def card_graph(cards, hidden=None):
    ''' This function draws the cards when displayed. '''
    card_len = len(cards)
    init(autoreset=True)

    if hidden is not None:

        print(
            f'{spacec}{colored("::::::::::",  color="white", on_color="on_blue")}' *
            2,
            end='')
        print('')
        print(
            f'{spacec}{colored("::      ::",  color="white", on_color="on_blue")}',
            end='')
        print(
            f'{spacec}{colored(f"::     {cards[1].suit}::",  color="white", on_color="on_blue")}')
        print(
            f'{spacec}{colored("::      ::",  color="white", on_color="on_blue")}' *
            2,
            end='')
        print('')
        print(
            f'{spacec}{colored("::HIDDEN::",  color="white", on_color="on_blue")}',
            end='')
        rank = cards[1].rank.rjust(2, ' ')
        print(
            f'{spacec}{colored(f"::  {rank}  ::",  color="white", on_color="on_blue")}',
            end='')
        print('')
        print(
            f'{spacec}{colored("::      ::",  color="white", on_color="on_blue")}' *
            2,
            end='')
        print('')
        print(
            f'{spacec}{colored("::      ::",  color="white", on_color="on_blue")}',
            end='')
        print(
            f'{spacec}{colored(f"::     {cards[1].suit}::",  color="white", on_color="on_blue")}')
        print(
            f'{spacec}{colored("::::::::::",  color="white", on_color="on_blue")}' *
            2,
            end='')
        print('')

    else:
        print(
            f'{spacec}{colored("::::::::::",  color="white", on_color="on_blue")}' *
            card_len,
            end='')
        print('')
        for i in range(0, card_len):
            print(
                f'{spacec}{colored(f"::     {cards[i].suit}::", color="white", on_color="on_blue")}',
                end='')
        print('')
        print(
            f'{spacec}{colored("::      ::",  color="white", on_color="on_blue")}' *
            card_len,
            end='')
        print('')
        for i in range(0, card_len):
            rank = cards[i].rank.rjust(2, ' ')
            print(
                f'{spacec}{colored(f"::  {rank}  ::",  color="white", on_color="on_blue")}',
                end='')
        print('')
        print(
            f'{spacec}{colored("::      ::",  color="white", on_color="on_blue")}' *
            card_len,
            end='')
        print('')
        for i in range(0, card_len):
            print(
                f'{spacec}{colored(f"::     {cards[i].suit}::", color="white", on_color="on_blue")}',
                end='')
        print('')
        print(
            f'{spacec}{colored("::::::::::",  color="white", on_color="on_blue")}' *
            card_len,
            end='')
        print('')


# In[5]:


class Player():

    ''' This class is to create a player and associated functions. '''

    count = 0

    def __init__(self, name):
        self.name = name
        self.bank = 1000
        #self.final_result = None
        self.blackjack = None

        Player.count += 1
        self.id = Player.count

        self.bet = 0  # start bet is zero when player created.
        print(
            f'{space}Player created.\n{space}Name : {self.name} \n{space}Balance : ${self.bank}')

        self.value = 0  # value at start is zero
        self.cards = list()

    @staticmethod
    def get_name():
        ''' This function is to get name of the player. '''
        while True:
            try:
                name = str(input(f'{space}Enter player\'s name :  '))
                if name in {''}:
                    raise ValueError
                if name.lower() == 'dealer':
                    print(f'{space}Player\'s name cannot be dealer!!')
                    continue
            except ValueError:
                print(f'{space}Player\'s name cannot be blank !!')
            else:
                break
        return name

    @staticmethod
    def get_bank(name):
        ''' This function is to get the purse value of the player. '''
        while True:
            try:
                bank = int(
                    input(f'{space}Hello {name}! Enter your purse value : $'))
                if bank < 100:
                    raise ValueError
            except ValueError:
                print(
                    f'{space}Purse value cannot be less than $100 / alphabets / blank.')
            else:
                break

        return bank

    def get_bet(self):
        ''' This function is to get the amount of bet player want's to set. '''
        while True:
            try:
                self.bet = int(
                    input(f'{space}Hello {self.name}! How much would you like to bet : $'))
                if self.bet > self.bank or self.bet < 10:
                    raise ValueError
            except ValueError:
                print(
                    f'{space}Bet value cannot be less than $10 or greater than the balance.')
            else:
                break

        ### Subtract the bet amount from the balance of the player ###
        self.bank -= self.bet
        print(
            f'{space}Bet placed for ${self.bet} by {self.name}. New balance : ${self.bank}')

    def set_value(self, special=None):
        ''' This function is to set value of player's cards as per the condition. '''
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
        ''' This function is to display player's cards. '''
        print(f'{space}     {self.name.upper()}\'s CARDS :\n')
        card_graph(self.cards)

        ### display soft hand ###
        soft_hand = None
        card_sum = sum([card.card_value() for card in self.cards])
        if '1' in [card.rank for card in self.cards]:
            if card_sum + 10 <= 21:
                soft_hand = card_sum + 10
            else:
                soft_hand = None

        if soft_hand is None or self.value == soft_hand:
            print('\n')
            print(f'{space}{self.name}\'s cards value : {self.value}')
        else:
            print('\n')
            print(f'{space}{self.name}\'s cards value : {self.value} or {soft_hand} ')
        print('\n')

    def cards_clear(self):
        ''' This function is to clear cards and value on replay. '''
        self.cards.clear()
        self.value = 0
        self.blackjack = None

    def black_win_bet(self):
        ''' This function is to set bank if player wins by blackjack. '''
        self.bank += (self.bet * 2.5)    # Bet + 3/2 bet

    def win_bet(self):
        ''' This function is to set bank if player wins. '''
        self.bank += (self.bet * 2)      # Bet + 1/1 bet

    def lose_bet(self):
        ''' This function is to set bank if player loses. '''
        self.bank = self.bank

    def tie_bet(self):
        ''' This function is to set bank if player ties. '''
        self.bank += self.bet

    def surrender_bet(self):
        ''' This function is to set bank if player surrenders. '''
        self.bank += (self.bet * 0.5)    # 1/2 Bet

    def insure_bet(self, outcome):
        pass


# In[6]:


class Dealer():

    ''' This class is to create a dealer and store his info. '''

    def __init__(self):
        self.value = 0
        self.cards = list()
        self.name = 'Dealer'
        self.blackjack = None

    def set_value(self):
        ''' This function is to set value of cards for the dealer as per the condition. '''
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
        ''' This function displays dealer's cards '''
        print(f'{space}     DEALERS\'s CARDS :\n')
        card_graph(self.cards, hidden)
        if hidden is None:
            print('\n')
            print(f'{space}Dealer\'s cards value : {self.value}')
        print('\n')

    def cards_clear(self):
        ''' This function is to clear cards and value on replay'''
        self.cards.clear()
        self.value = 0
        self.blackjack = None


# In[7]:


class Card():

    ''' This class is to create a card instance using suit and rank. '''

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def card_value(self):
        ''' This function returns the value of a card. '''
        return values[self.rank]


# In[8]:


class Deck():

    ''' This class is to create a deck of cards. '''

    def __init__(self):
        self.deck = list()
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))  # 52 card objects created
        random.shuffle(self.deck)
        print(f'{space}Deck created and shuffled.')

    def shuffle(self):
        ''' This function is used to shuffle the deck. '''
        random.shuffle(self.deck)

    def draw(self):
        ''' This function is to draw initial card from the deck. Gamer is either players or dealer object. '''
        return self.deck.pop(), self.deck.pop()  # pop two cards from the deck list and return

    def hit(self):
        ''' This function is to hit the deck. '''
        return self.deck.pop()   # Pop card from the deck objects deck


# In[9]:


def graffiti(result):
    ''' This function is to draw graffiti at the start and end of game. '''
    print('\n')
    print(
        pyfiglet.figlet_format(
            result.upper(),
            font='slant',
            width=100,
            justify='center'))
    print('\n')


# In[10]:


def cases(player, dealer, result):
    '''
    This function receives input check result and declares the result as per check case.

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
        print(f'{space}{player.name} hits BLACKJACK !')
        print(f'{space}Checking dealer\'s cards.....   ', end='')
        print(f'{space}Dealer hits BLACKJACK as well !')
        print(f'{space}{player.name} and dealer PUSH ! Game tie !')
        graffiti('push')
    elif result == 1:
        print('\n\n')
        print(
            f'{space}{player.name} hits BLACKJACK ! {player.name} WINS ! Congratulations !')
        graffiti('win')
    elif result == 2:
        print('\n\n')
        print(f'{space}Dealer\'s hit BLACKJACK ! {player.name} LOST !')
        graffiti('lost')
    elif result == 3:
        print('\n\n')
        print(f'{space}{player.name} BUST ! {player.name} LOST !')
        graffiti('lost')
    elif result == 4:
        print('\n\n')
        print(f'{space}Dealer\'s hit BLACKJACK ! {player.name} LOST !')
        graffiti('lost')
    elif result == 5:
        print('\n\n')
        print(f'{space}Dealer BUST ! {player.name} WINS !')
        graffiti('win')
    elif result == 6 or result == 10:
        print('\n\n')
        print(f'{space}{player.name} and dealer PUSH ! Game tie !')
        graffiti('push')
    elif result == 7 or result == 8:
        print('\n\n')
        print(
            f'{space}{player.name} WINS ! {player.name}\'s cards have greater value ! Congratulations !')
        graffiti('win')
    elif result == 9:
        print('\n\n')
        print(f'{space}{player.name} LOST ! Dealer\'s cards have greater value !')
        graffiti('lost')
    elif result == 11:
        print('\n\n')
        print(f'{space}{player.name} SURRENDERED !!')
        graffiti('surrender')


# In[11]:


def blackjack_check(dealer, player):
    ''' This function is to check blackjack condition. '''
    if player.value == 21 and dealer.value == 21:
        return 0
    elif player.value == 21:
        return 1
    elif dealer.value == 21:
        return 2
    else:
        return 100


# In[12]:


def top_check(dealer, player):
    ''' This function is to check special case where player has 21 but dealer has blackjack. '''
    if player.value == 21 and dealer.blackjack:
        return 4
    elif player.value == 21:
        return 100  # not complete result , needs to stand


# In[13]:


def bust_check(dealer=None, player=None):
    ''' This function is to check the bust condition. '''
    if dealer is not None:
        if dealer.value > 21:
            return 5
    elif player is not None:
        if player.value > 21:
            return 3

    return 101


# In[14]:


def win_check(dealer, player):
    ''' This function is to check who wins in case there is no blackjack or bust. '''
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


# In[15]:


def surrender_check(dealer, player):

    surr = surrender_or_play(player)
    check, hors = None, None
    if surr in {'s', 'surrender'}:
        print(f'{space}Checking if dealer has a blackjack.....\n')
        if dealer.blackjack:
            print(f'{space}Cannot surrender, dealer has a BLACKJACK ! ')
            check = 2
            hors = 'as'       # Auto Stand
        else:
            check = 11
            hors = None

    return check, hors


# In[16]:


def hit_or_stand(player):
    ''' This function is to check users choice regarding hit or stand. '''
    hors = str(
        input(f'{space}{player.name}, Do you want to hit or stand ? [H/S] : ')).lower()
    while hors not in {'h', 's', 'hit', 'stand'}:
        hors = str(
            input(f'{space}{player.name}, Enter hit or stand only ? [H/S] : ')).lower()
    return hors


# In[17]:


def surrender_or_play(player):

    surr = str(input(
        f'{space}{player.name}, Do you want to surrender or play ? [S/P] : ')).lower()
    while surr not in {'p', 's', 'play', 'surrender'}:
        surr = str(
            input(f'{space}{player.name}, Enter surrender or play ? [S/P] : ')).lower()
    return surr


# In[18]:


def display_cards(dealer, player, hidden=None):
    ''' This function is to display cards. '''
    clearscreen()  # changed
    print('\n' * 3)
    dealer.display(hidden=hidden)
    player.display()


# In[19]:


class Highscores():

    ''' This class is a collection of methods to handle highscores. '''

    @staticmethod
    def load_highscores():
        ''' This function is to load highscores once the game starts. '''
        if os.path.exists('scoresdb'):
            highscores = pd.read_csv('scoresdb')
        else:
            highscores = pd.DataFrame(columns=['Rank', 'Name', 'Score'])

        return highscores

    @staticmethod
    def update_highscores(highscores, player):
        ''' This function is to update the highscore as well as store it. '''
        ### Add score to highscores ###
        highscores.loc[len(highscores)] = [None, player.name, player.bank]

        ### Sort the highscores ###
        highscores.sort_values(
            by='Score',
            ascending=False,
            inplace=True,
            ignore_index=True)

        ### Update rank according index ###
        highscores['Rank'] = list(range(1, len(highscores) + 1))
        highscores = highscores.head(10)

        ### Update scoresdb file ###
        highscores.to_csv('scoresdb', index=False)
        return highscores

    @staticmethod
    def display_highscores(highscores):
        ''' This function is to display the highscores after game ends. '''
        print(f'{space}    \t  HIGHSCORES :  \t      \n')
        for row in highscores.to_string(index=False).split('\n'):
            print(space + row)


# In[20]:


def game(replay=None, players=None, dealer=None):
    ''' This function is to conduct the game. '''
    ### Create players for the game ###
    if replay is None:
        players = list()   # For supporting multiplayer in future

        name = Player.get_name()
        # Player created and appended to playes list
        players.append(Player(name))

        ### Create a dealer for the game ###
        dealer = Dealer()

    else:
        ### Remember players if replay and clear cards ###
        players = players
        for player in players:
            player.cards_clear()
        dealer.cards_clear()

    ### Setup deck ###
    play_deck = Deck()

    ### Bet amount ###
    player1 = players[0]  # Since currently single player game
    player1.get_bet()

    ### Draw the cards for dealer and players ###
    for card in play_deck.draw():
        dealer.cards.append(card)
    dealer.set_value()

    for card in play_deck.draw():
        player1.cards.append(card)
    player1.set_value()

    ### Display cards and values ###
    display_cards(dealer, player1, hidden='x')

    ##### PENDING : Concept of insurance ##########
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

    ### Player has a blackjack or both have. Game end. ###
    if check in {0, 1}:
        time.sleep(2)
        display_cards(dealer, player1)
        cases(player1, dealer, check)

    ### Dealer has a blackjack or no one has. Game continue. ###
    else:

        ### Allow player to surrender if dealer does not have a blackjack ###
        check, hors = surrender_check(dealer, player1)

        while True:

            ### Surrendered ###
            if check == 11:
                display_cards(dealer, player1)
                break

            ### Auto stand if player reaches 21 else ask ###
            if hors != 'as':
                hors = hit_or_stand(player1)

            ### Player Hits ###
            if hors in {'h', 'hit'}:

                # player1.cards is a list, an atribute of player1 object
                player1.cards.append(play_deck.hit())
                player1.set_value()
                display_cards(dealer, player1, hidden='x')

                # check if player1 is bust # check will be 3 if player busts
                check = bust_check(player=player1)
                if check == 3:
                    break

                check = top_check(dealer, player1)
                if check == 4:                          # player hits 21 and dealer hits blackjack
                    break
                elif check == 100:                      # player hits 21 , needs to auto stand.
                    hors = 'as'
            ### Player stands ###
            elif hors in {'s', 'stand', 'as'}:

                if dealer.blackjack:
                    check = 2                           # dealer blackjack restore
                    display_cards(dealer, player1)
                    break

                ### Special ace case ###
                ### If player has ace in his cards, sum of cmp(soft,hard) must be taken ###
                ### EX : player 1,7  dealer 7,9 ###
                player1.set_value(special=True)

                while dealer.value < 17:
                    dealer.cards.append(play_deck.hit())
                    dealer.set_value()
                    display_cards(dealer, player1)
                    time.sleep(1)

                display_cards(dealer, player1)

                # check if dealer is bust
                check = bust_check(dealer=dealer)
                if check == 5:
                    break

                check = win_check(dealer, player1)      # comparison check
                if check != 102:
                    break

        cases(player1, dealer, check)

    ### Bank update ###
    if check in {0, 6, 10}:
        player1.tie_bet()
    elif check in {2, 3, 4, 9}:
        player1.lose_bet()
    elif check in {5, 7, 8}:
        player1.win_bet()
    elif check in {11}:
        player1.surrender_bet()
    else:
        player1.black_win_bet()

    return players, dealer      # for replay


# In[21]:


def main():
    ''' This function controls everything '''

    ### Welcome ###
    print(f'{space}Welcome to BLACKJACK.')
    print('\n')
    # game_help()
    H = Highscores()

    ### Load highscores ###
    highscores = H.load_highscores()

    ### Start ###
    while True:

        print(f'{space}Are you ready to play the game ? : [Y/N] ', end='')
        try:
            start = str(input()).lower()
            if start not in {'y', 'n', 'yes', 'no'}:
                raise ValueError
        except ValueError:
            print(f'{space}Enter either Y or N.')
        else:
            if start in {'y', 'Y'}:
                clearscreen()  # changed  #100
                print('\n' * 3)
                players, dealer = game()

                while True:  # Replay Loop ### TRY CATCH rmaining ###

                    player1 = players[0]
                    print('\n')
                    print(
                        f'{space}Player score : \n{space}Name : {player1.name} \n{space}Balance : ${player1.bank}')
                    print('\n')

                    ### If bank goes below 10 should not allow to play ###

                    if player1.bank <= 10:
                        print(
                            f'{space}Bank balance is below the minimum of $10 required')
                        break

                    ### Else ask for replay ####
                    replay = str(
                        input(f'{space}Play once again ? : [Y/N] ')).lower()
                    if replay in {'y', 'yes'}:
                        players, dealer = game(
                            replay=replay, players=players, dealer=dealer)
                    elif replay in {'n', 'no'}:
                        start = 'n'
                        print('\n')
                        print(
                            f'{space}Final score : \n{space}Name : {player1.name} \n{space}Balance : ${player1.bank}')
                        print('\n')

                        ### Update and Display highscores ###
                        highscores = H.update_highscores(highscores, player1)
                        time.sleep(1)
                        clearscreen()  # changed
                        print('\n' * 3)
                        print(
                            pyfiglet.figlet_format(
                                'GoodBye',
                                font='slant',
                                width=100,
                                justify='center'))
                        print('\n' * 3)
                        H.display_highscores(highscores)
                        print('\n' * 3)
                        break
                    else:
                        continue

            else:
                print(f'{space}Bye. Have a nice day !!!')
            break


# In[ ]:


try:
    terminal = get_ipython().__class__.__name__
except Exception:
    pass
else:
    if get_ipython().__class__.__name__ == 'ZMQInteractiveShell':
        get_ipython().system('jupyter nbconvert --to python blackjack.ipynb')
        get_ipython().system('pylint blackjack.py')
        get_ipython().system('autopep8 --in-place --aggressive blackjack.py')
        get_ipython().system('pylint blackjack.py  ')
finally:
    if __name__ == "__main__":
        main()
