# Uno Card Game with GUI
# Author: Andrew Linn
# Updated 1/7/2020
# Version 2.0
#
# Rules:
# Set up: 2-10 players, each player starts with 7 cards in their hand, a number card is put on top of the discard pile,
# a random player is selected to go first
#
# Gameplay: You must play a card that has either the same number/type or color as the card on top of the discard pile.
# If you cannot, you must draw a card and lose your turn. If you draw a card that can be played, it will be played.
# Reverse cards change the direction of play. Skip cards skip the next player's turn. Draw 2 cards make the next player
# draw 2 cards and then skip their turn. Wild cards allow you to change the color to anything you want. Wild draw 4
# cards allow you to change the color, have the next player draw 4 cards, and then skip their turn.

import random
import pygame
import sys
import os

# The class for a card, where each card has a color and a type
class UnoCard:
    def __init__(self, color, card_type):
        self.card_color = color
        self.card_type = card_type

    def __str__(self):
        return f'{self.card_color} {self.card_type}'

    __repr__ = __str__

# The class for a player, where each player has a name and a hand
class Player:
    def __init__(self, name, hand):
        self.name = name
        self.hand = hand

    def __str__(self):
        return f'{self.name} has a hand of {self.hand}'

    __repr__ = __str__


# Cards that have not been played
deck = []
# All players playing
players_list = []
# Cards that have been played, where the last card in the list is the one on top of the pile
discard_pile = []
# The direction of play. Changes with a reverse card. Can be 'clockwise' or 'counterclockwise'
play_direction = 'clockwise'


# Start Pygame
pygame.init()
# Create the Pygame window
window_width = 800
window_height = 600
screen = pygame.display.set_mode((window_width, window_height))
# Title of the window
pygame.display.set_caption('Uno')


# This function will reverse the direction of play when a reverse card is used
def reverse_play_direction():
    global play_direction
    if play_direction == 'clockwise':
        play_direction = 'counterclockwise'
    else:
        play_direction = 'clockwise'
    print('\n\nChanging directions!')

# This function will create the Uno deck.
def create_deck():
    card_colors = ['blue', 'red', 'green', 'yellow']
    colored_cards = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'picker', 'skip'
        , 'reverse']
    # Create cards of each color and type for the deck
    for color in card_colors:
        for card_type in colored_cards:
            if card_type is 'zero':
                # Uno decks only have one 0 card of each color
                deck.append(UnoCard(color, card_type))
            else:
                # Every other colored card appears twice in an Uno deck
                deck.append(UnoCard(color, card_type))
                deck.append(UnoCard(color, card_type))
    # Add 4 wild cards and 4 wild draw 4 cards to the deck
    for i in range(4):
        deck.append(UnoCard('wild', 'color_changer'))
        deck.append(UnoCard('wild', 'pick_four'))
    return deck

# This function will determine if the deck is empty
def is_deck_empty():
    if deck:
        return False
    else:
        return True

# This function will draw a card for a player
def draw_card(Player):
    # If the deck is empty: add all the cards from the discard pile (except the last(top) one) back to the deck
    if is_deck_empty():
        for discard_card_index in range(0, len(discard_pile) - 2):
            deck.append(discard_pile.pop(discard_card_index))
    # Get the index of the card to be drawn
    card_index = random.randint(0, len(deck) - 1)
    # Get the card at that index and add it to the hand
    card = deck.pop(card_index)
    Player.hand.append(card)
    return card

# This function will create a starting hand for a player
def create_hand():
    hand = []
    # Draw 7 cards for a starting hand
    for draw_card in range(7):
        # Get the index of the card to be drawn
        card_index = random.randint(0, len(deck) - 1)
        # Get the card at that index and add it to the hand
        card = deck.pop(card_index)
        hand.append(card)
    return hand

# This function will create the players for the game and give each one a starting hand
# In Uno there is between 2 and 10 players
def create_players():
    # Get the number of players playing
    valid_players = False
    while not valid_players:
        number_of_players = input('How many players are playing? (Enter an integer between 2 and 10): ')
        if number_of_players.isnumeric() and 2 <= int(number_of_players) <= 10:
            number_of_players = int(number_of_players)
            valid_players = True
    # Create a Player for each player with a starting hand
    for player in range(number_of_players):
        # Get the name of the player
        valid_name = False
        while not valid_name:
            player_name = input(f'Enter the name for player {player + 1}: ')
            if not player_name.isspace() and player_name != '':
                valid_name = True
        # Create a hand for the player
        hand = create_hand()
        # Create a Player and add it to the players_list
        players_list.append(Player(player_name, hand))
    return players_list

# This function creates the starting discard pile. The first card must be a number.
def create_start_dis_pile():
    invalid_types = ['wild', 'wild draw 4', 'draw two', 'skip', 'reverse']
    valid_starter = False
    # Select a random card from the deck until you get one that is a number
    while not valid_starter:
        # Get the index of the card to be drawn
        card_index = random.randint(0, len(deck) - 1)
        # Get the card at that index
        card = deck[card_index]
        # Check if that card is a valid card to start on
        if card.card_type not in invalid_types:
            valid_starter = True
            discard_pile.append(deck.pop(card_index))
    return discard_pile

# This function will determine if a valid move was made. A valid move is when a player plays a card with the same color
# or type as the card that is on top of the discard pile, or if the card is wild.
########################################################################################################################
# Notes:
# A card is found by using players_list[player index].hand[card index] (ex: players_list[0].hand[0])
# A card's color or type is found by using players_list[player index].hand[card index].something where something is
# either card_color or card_type
def is_valid_move(card):
    if card.card_type == discard_pile[-1].card_type or card.card_color == discard_pile[-1].card_color or card.card_color == 'wild':
        return True
    else:
        return False

# This function will play a card
def play_card(player_index, card_index):
    # Take the played card out of the player's hand and add it to the discard pile
    played_card = players_list[player_index].hand.pop(card_index)
    discard_pile.append(played_card)
    return discard_pile

# This function will go through a turn for a player
def play_turn(current_player_index):
    # OLD - Set up hand in console
    print(f'\n\n*** It is {players_list[current_player_index].name}\'s turn. ***')
    print('The top card is: ', discard_pile[-1])
    hand_statement = f'{players_list[current_player_index].name}\'s cards:'
    card_number = 1
    for card in players_list[current_player_index].hand:
        hand_statement += f'   {card_number}.) {card}'
        card_number += 1
    print(hand_statement)
    cards_in_players_hand = len(players_list[current_player_index].hand)

    # Pygame - Set up hand on screen
    # Start 10 pixels from the left
    l_start_pixel = 10
    for card in players_list[current_player_index].hand:
        # Construct the filename of the card that will be displayed on screen
        filename = str(card.card_color) + '_' + str(card.card_type) + '_tiny.png'
        print(filename)
        # Display the card on the screen
        load_card = pygame.image.load(os.path.join('PNGs\\tiny', filename))
        screen.blit(load_card, (l_start_pixel, window_height - 91))
        l_start_pixel += 65
        pygame.display.update()

    valid_input = False
    while not valid_input:
        decision = input('Enter the number of the card you want to play, or type \'d\' to draw a card.')
        # If the user wants to draw a card:
        if decision == 'd':
            print(f'{players_list[current_player_index].name} will draw a card.')
            # Draw a card and see if it can be played
            card_drawn = draw_card(players_list[current_player_index])
            # If the card drawn can be played, play it
            if is_valid_move(card_drawn):
                print(f'{players_list[current_player_index].name} drew a {card_drawn} that can be played!')
                play_card(current_player_index, -1)
                card_type = discard_pile[-1].card_type
                return card_type
            # If it can't be played, just add it to hand
            return None
        # If the user wants to play a card:
        elif decision.isnumeric():
            if 1 <= int(decision) <= cards_in_players_hand:
                # Check if the move is valid
                if is_valid_move(players_list[current_player_index].hand[int(decision) - 1]):
                    play_card(current_player_index, int(decision) - 1)
                    # Get the type of the card that was just played to see if there are extra actions to be done now
                    # like +2, skip, etc.
                    card_type = discard_pile[-1].card_type
                    return card_type
                print('Sorry, that move is not valid. If you have no valid moves please draw a card.')

# This function will change the color of a wild card when it is played
def change_color():
    # OLD TEXT-BASED WAY TO CHANGE
    # valid_input = False
    # valid_inputs = ['blue', 'yellow', 'green', 'red']
    # while not valid_input:
    #     new_color = input('Wild card played! What color should it be?: ')
    #     if new_color.lower() in valid_inputs:
    #         valid_input = True

    discard_pile[-1].card_color = new_color

# This function will advance the turn based on the direction of play (that is changed with a reverse card)
def advance_turn(current_player_index):
    index = current_player_index
    number_of_players = len(players_list)
    if play_direction == 'clockwise':
        index += 1
        if index > (number_of_players - 1):
            index = 0
    elif play_direction == 'counterclockwise':
        index -= 1
        if index < 0:
            index = (number_of_players - 1)
    return index

# This function will play the game
def play_uno():
    # Create the Uno deck, players, and discard pile
    create_deck()
    create_players()
    create_start_dis_pile()

    # Display the back of an uno card that can be clicked on to draw a card
    screen.blit(pygame.image.load(os.path.join('PNGs\\small', 'card_back.png')), (42, 100))

    # The index of the player who's turn it is (This determines who goes first at random)
    current_player_index = random.randint(0, len(players_list) - 1)

    # Play until the game is won (a player has no cards)
    game_won = False
    while not game_won:
        # Actions that are done in the game
        for event in pygame.event.get():
            # Lets you quit out with the x
            if event.type == pygame.QUIT:
                sys.exit()

        # Update the top card of the discard pile
        # Construct the filename of the card that will be displayed on screen
        top_filename = str(discard_pile[-1].card_color) + '_' + str(discard_pile[-1].card_type + '.png')
        print(top_filename)
        # Display the card on the screen
        load_top_card = pygame.image.load(os.path.join('PNGs\\small', top_filename))
        screen.blit(load_top_card, (172, 100))

        # Call the play_turn function to play a Player's turn (returns the type of card played for further action)
        played_card_type = play_turn(current_player_index)

        # OLD
        # If a wild card is played, change the color of the top card
        if played_card_type == 'wild':
            change_color()
        # If a skip card is played, advance the turn twice to skip the next player
        if played_card_type == 'skip':
            current_player_index = advance_turn(current_player_index)
            print(f'\n\nSkipping {players_list[current_player_index].name}\'s turn!')
        # If a reverse card is played, reverse the direction of play
        if played_card_type == 'reverse':
            reverse_play_direction()
        # If a draw two card is played, have the next player draw 2 cards, then skip their turn
        if played_card_type == 'draw two':
            current_player_index = advance_turn(current_player_index)
            print(f'\n\n{players_list[current_player_index].name} draws two cards and loses their turn!')
            draw_card(players_list[current_player_index])
            draw_card(players_list[current_player_index])
        # If a wild draw 4 card is played, change the color, have the next player draw 4 cards, then skip their turn
        if played_card_type == 'wild draw 4':
            change_color()
            current_player_index = advance_turn(current_player_index)
            print(f'\n\n{players_list[current_player_index].name} draws four cards and loses their turn!')
            for i in range(4):
                draw_card(players_list[current_player_index])
        # Advance the turn once
        current_player_index = advance_turn(current_player_index)
        # The game is won when a player runs out of cards. Check if there is a winner:
        for player in players_list:
            if len(player.hand) == 0:
                game_won = True
                print(f'\n\n*** Congratulations, {player.name} has won the game! ***')

        pygame.display.update()


# Start the game
play_uno()

