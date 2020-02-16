#!/usr/bin/env python
# coding: utf-8

# In[1]:


'''
Blackjack game.
'''
import random


# In[2]:


ranks = (
    '1',
    '2',
    '3',
    '4',
    '5',
    '6',
    '7',
    '8',
    '9',
    '10',
    'Jack',
    'Queen',
    'King')
suits = ('Spade', 'Clover', 'Diamond', 'Heart')
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
    'Jack': 10,
    'Queen': 10,
    'King': 10}


# In[3]:


class game_help():
    pass


# In[4]:


class Player():

    ''' This class is to create a player. '''
    count = 0

    def __init__(self, name, bank):
        self.name = name
        self.bank = bank

        Player.count += 1
        self.id = Player.count

        self.bet = 0  # start bet is zero when player created.
        print(
            f'Player No. {self.id} created. Name : {self.name} , Balance : {self.bank}')

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

    def set_value(self):

        # Ace present check for blackjack condition , Note cards are objects
        if '1' in [card.rank for card in self.cards]:
            if sum([card.card_value() for card in self.cards]
                   ) == 11:  # If ace is considered as 11, value will be 11 + 10
                self.value = 21
        else:
            self.value = sum([card.card_value() for card in self.cards])

    def display(self):

        print(f'{self.name} has the following cards :')
        print(f'######################################################')
        for card in self.cards:
            print(f'# {card.rank} of {card.suit}  ', end='')
            print('#')
        print(f'######################################################')
        print('\n')

    def win_bet(self, bet):
        pass

    def lose_bet(self, bet):
        pass

    def increase_value(self):
        pass


# In[5]:


class Dealer():

    ''' This class is to create a dealer and store his info. '''

    def __init__(self):
        self.value = 0
        self.cards = list()
        self.name = 'Dealer'

    def set_value(self):

        #######self.value = sum([ card.card_value() for card in self.cards ])
        # print(self.value)
        # Ace present check for blackjack condition , Note cards are objects
        if '1' in [card.rank for card in self.cards]:
            if sum([card.card_value() for card in self.cards]
                   ) == 11:  # If ace is considered as 11, value will be 11 + 10
                self.value = 21
        else:
            self.value = sum([card.card_value() for card in self.cards])

    def display(self):

        print(f'Dealer has the following cards :')
        print(f'######################################################')
        if len(self.cards) == 2:  # This is the initial display
            print(
                f'# {self.cards[0].rank} of {self.cards[0].suit}  # XX HIDDEN XX #')
        else:
            for card in self.cards:
                print(f'# {card.rank} of {card.suit}  ', end='')
                print('#')
        print(f'######################################################')
        print('\n')


# In[6]:


class Card():

    ''' This class is to create a card instance using suit and rank. '''

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def card_value(self):
        return values[self.rank]


# In[7]:


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

    def draw(self, gamer):
        ''' This function is to draw initial card from the deck. Gamer is either players or dealer object. '''
        return self.deck.pop(), self.deck.pop()  # pop two cards from the deck list and return
        # print(len(self.deck))                      #lenght for debug

    # def hit(self,gamer):
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
# 8. add create py file in ipynb
# 9. better replay looping
#
#
# ### future ###
# 1. insurance
# 2. split
# 3. double down
# 4. multiplayer
# 5. multideck
# 6. pygame  : In future, display game using pygame library.
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

# In[8]:


def printing(player, result):

    def graffiti(result):
        print('\n\n')
        print('########')
        print(result.upper())
        print('########')
        print('\n\n')

    if result == 'pushb':              # Blackjack push or tie
        print('\n\n')
        print(f'Blackjack for {player.name} !')
        for x in range(0, 5):
            print('Checking dealer;s cards.....', end='')
        print(f'Blackjack for dealer as well !')
        graffiti('push')
    elif result == 'push':             # Normal push or tie
        print('\n\n')
        print(f'Tie for {player.name} and dealer ! Game tie !')
        graffiti('push')
    elif result == 'bustd':             # Win for player. Bust for dealer.
        print('\n\n')
        print(f' Dealer BUST ! Player {player.name} won !')
        graffiti('win')
    elif result == 'bust':             # Loss for player by bust.
        print('\n\n')
        print(f' {player.name} BUST ! Player {player.name} lost !')
        graffiti('lost')
    elif result == 'lost':             # Loss of player
        print('\n\n')
        print(
            f'Dealer\'s cards have greater value ! Player {player.name} lost !')
        graffiti('lost')
    elif result == 'lostb':            # Loss of player to dealer's blackjack
        # special case of lost where when dealer is using stand , dealer draws
        # a blackjack ###
        print('\n\n')
        print(f'Dealer\'s hit blackjack ! Player {player.name} lost !')
        graffiti('lost')
    elif result == 'winb':                 # Win with blackjack for player
        print('\n\n')
        print(
            f'Blackjack for {player.name} ! Player {player.name} wins ! Congratulations !')
        graffiti('win')
    elif result == 'win':                 # Normal win for player
        print('\n\n')
        print(
            f'Player {player.name}\'s cards have greater value ! Player {player.name} wins ! Congratulations !')
        graffiti('win')
    else:
        print('\n\n')


# In[9]:


def blackjack_check(dealer, player):

    ### CASE 1 : Player draws a blackjack at first draw ###
    ## SUB CASE 1 : player and dealer both hit blackjack : WINCHECK -> PUSH ##
    if player.value == 21 and dealer.value == 21:
        return 'pushb'
    elif player.value == 21:
        return 'winb'
    elif dealer.value == 21:
        return 'lostb'
    else:
        return 'na'


# In[10]:


def bust_check(dealer=None, player=None):

    if dealer is not None:
        if dealer.value > 21:
            return 'bustd'
        else:
            return 'na'
    elif player is not None:
        if player.value > 21:
            return 'bust'
        else:
            return 'na'


# In[11]:


def win_check(dealer, player):

    return 'win' if dealer.value < player.value else 'lost' if dealer.value > player.value else 'push'
    # This push is a tie, Not a blackjack push


# In[12]:


def hit_or_stand(player):

    hors = str(input(f'{player.name}, Do you want to hit or stand ? [H/S] :'))
    while hors.lower() not in {'h', 's', 'hit', 'stand'}:
        hors = str(input(f'{player.name}, Enter hit or stand only ? [H/S] :'))
    return hors


# In[13]:


def game():
    ''' This function is to conduct the game. '''
    ### Create players for the game ###
    players = list()   # For supporting multiplayer in future
    name = Player.get_name()
    bank = Player.get_bank(name)
    # Player created and appended to playes list
    players.append(Player(name, bank))

    ### Create a dealer for the game ###
    dealer = Dealer()

    ### Setup deck ###
    play_deck = Deck()
    # print([(x.suit,x.rank) for x in play_deck.deck ])  #print deck for debug

    ### Bet amount ###
    player1 = players[0]  # Since currently single player game
    player1.get_bet()

    ### Draw the cards for dealer and players ###
    for card in play_deck.draw(dealer):
        dealer.cards.append(card)
    dealer.set_value()
    # print(f'Initial dealer value {dealer.value}') # debug

    for card in play_deck.draw(player1):
        player1.cards.append(card)
    ##### Inducing ace #### REMOVE AFTERWARDS ######
    # player1.cards[0] = Card('Spade','1')  #debug
    # player1.cards[1] = Card('Spade','10') # debug
    player1.set_value()
    # print(f'Initial player value : {player1.value}')   # debug

    ### Display cards and values ###
    print('\n\n' * 100)
    dealer.display()
    player1.display()

    ### Win check ###  ### this needs to be improved ### Special check 1st instance ###
    ##### PENDING #####
    # EVEN IF DEALER HAS BLACK JACK IN DRAW, PLAYERS NEED TO PLAY, ONLY when they stand, dealer reveals bj
    ##### Concept of insurance ##########
    bcheck = blackjack_check(dealer, player1)
    # print({player1.value})   # debug
    # print(f'{bcheck}')       # debug
    printing(player1, bcheck)
    if bcheck == 'na':  # if initial check is ok

        while True:
            hors = hit_or_stand(player1)
            if hors in {'h', 'hit'}:
                # player1.cards is a list, an atribute of player1 object
                player1.cards.append(play_deck.hit())
                print(player1.value)
                player1.set_value()

                dealer.display()
                player1.display()

                bcheck = blackjack_check(
                    dealer, player1)    # check if blackjack
                printing(player1, bcheck)
                if bcheck != 'na':
                    break

                # check if player1 is bust
                bucheck = bust_check(player=player1)
                # print(player1.value)          #debug
                # print(f'{bucheck} buchec')    #debug
                printing(player1, bucheck)
                if bucheck != 'na':
                    break

            elif hors in {'s', 'stand'}:
                print(dealer.value)
                while dealer.value < 17:
                    dealer.cards.append(play_deck.hit())  # NOT WORKING ###
                    dealer.set_value()
                dealer.display()
                player1.display()

                bcheck = blackjack_check(
                    dealer, player1)  # check if black jack
                # print(f'bcheck {bcheck}')   #debug
                printing(player1, bcheck)
                if bcheck != 'na':
                    break

                # check if dealer is bust
                bucheck = bust_check(dealer=dealer)
                printing(dealer, bucheck)
                if bucheck != 'na':
                    break

                wcheck = win_check(dealer, player1)
                # print(f'wcheck : {wcheck}')  # debug
                printing(player1, wcheck)
                break


# In[15]:


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
                while True:  # Replay Loop ### TRY CATCH rmaining ###
                    game()
                    replay = str(input('Play once again ? : [Y/N] '))
                    if replay in {'y', 'yes'}:
                        continue
                    else:
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
