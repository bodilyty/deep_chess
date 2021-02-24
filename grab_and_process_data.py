import random
import chess
import pgn
import sys
import os
import numpy as np
from keras import layers
from keras import models
from random import randrange
import re
import csv

os.chdir('/Users/tybodily/projects/deep_chess/')

random.seed(1)

def shorten_string(s):
    s = s[:s.rfind(" ")]
    return s

def fen_to_bit(f):
    pieces = {
        'p': 1,
        'P': 7,
        'n': 2,
        'N': 8,
        'b': 3,
        'B': 9,
        'r': 4,
        'R': 10,
        'q': 5,
        'Q': 11,
        'k': 6,
        'K': 12
            }
    
    f = shorten_string(f)

    for i in range(2):
        f = shorten_string(f)

    piece_squares = np.zeros(64)
    ranks = shorten_string(shorten_string(f)).split('/')
    
    for rank_count,rank in enumerate(ranks):
        #print(rank_count)
        file_count = 0
        for item in rank:

            if item.isnumeric():
                file_count += int(item)
            else:
                piece_squares[(file_count + (8 * (rank_count)))] = pieces[item]
                file_count += 1
    
    all_bits = np.zeros(64*12)
    for c,square in enumerate(piece_squares):
        if square > 0:
            all_bits[int((max((square-1),0) * 64) + c)] = 1
            
    to_move = shorten_string(f)[-1]
    if to_move == 'w':
        all_bits = np.append(all_bits,1)
    else:
        all_bits = np.append(all_bits,0)
    
    castle = f[-4:]
    for letter in 'KQkq':
        if letter in castle:
            all_bits = np.append(all_bits,1)
        else:
            all_bits = np.append(all_bits,0)
    return(all_bits)








# print('loading file...')
# # f = open('./games/CCRL-4040.[1144921].pgn')
# # pgn_text = f.read()
# # f.close()
# f = open('./output.txt')
# file = f.read()
# f.close()

# m = re.split('\n\n',file)

# print('parsing games...')
# parsed_games = []
# for num in range(len(m)):
#     if num%100000 == 0:
#         print(num)
#     if num%2 == 1:
#         unparsed_game = m[num].replace('\n',' ')
#         new_game = []
#         for entry in unparsed_game.split(' '):
#             if entry[-1]!='.':
#                 new_game.append(entry)
#         parsed_games.append(new_game)


# games = parsed_games.copy()

# print('finding draws...')
# no_draws = []
# for game in games:
#     if game[-1] != '1/2-1/2':
#         no_draws.append(game)


# print('splitting white and black wins')
# white_wins = []
# black_wins = []
# count = 0
# for game in no_draws:
#     if count%10000 == 0:
#         print(count)
#     if len(game) < 10:
#         print('short game')
#     if game[-1] == '1-0':
#         white_wins.append(game[:-1])
#     if game[-1] == '0-1':
#         black_wins.append(game[:-1])
#     count =+1

# print('number of white games:',len(white_wins))
# print('number of black games:',len(black_wins))

# print('\nselecting random positions from games...')
# #select 10 random positions per game
# black_positions = []
# white_positions = []
# count = 0
# for game in white_wins:
#     if count%10000 == 0:
#         print('white games:',count)
#     num=0
#     #select 10 random positions:
#     while num <10:
#         potential_position = game[0:np.random.randint(5,len(game))]
#         #print(potential_position)
#         if 'x' in potential_position[-1]:
#             continue
#         else:
#             white_positions.append(potential_position)
#             #print('good position',potential_position)
#             num+=1
#     count +=1
# count = 0
# for game in black_wins:
#     if count%10000 == 0:
#         print('black games:',count)
#     num=0
#     #select 10 random positions:
#     while num <10:
#         potential_position = game[0:np.random.randint(5,len(game))]
#         #print(potential_position)
#         if 'x' in potential_position[-1]:
#             continue
#         else:
#             black_positions.append(potential_position)
#             #print('good position',potential_position)
#             num+=1
#     count += 1


# with open(f'random_white_positions_{len(white_positions)}.csv',"w") as f:
#     wr = csv.writer(f,delimiter=",")
#     wr.writerows(white_positions)

# with open(f'random_black_positions_{len(black_positions)}.csv',"w") as f:
#     wr = csv.writer(f,delimiter=",")
#     wr.writerows(black_positions)

print('loading data...')
white_positions = []
with open('random_white_positions_3956350.csv') as csvfile:
    r = csv.reader(csvfile, delimiter=',')
    for row in r:
        white_positions.append(row)

black_positions = []
with open('random_black_positions_2928400.csv') as csvfile:
    r = csv.reader(csvfile, delimiter=',')
    for row in r:
        black_positions.append(row)


print('getting bits...')
#num_positions = 1000000
white_bits = np.zeros((len(white_positions),773))
black_bits = np.zeros((len(black_positions),773))

count = 0

for white_position in white_positions:
    if count%100000 == 0:
        print(count)
    board = chess.Board()
    for move in white_position:
        board.push_san(move)
    
    white_bit = fen_to_bit(board.fen())
    white_bits[count,:] = white_bit
    count +=1

count = 0

for black_position in black_positions:
    if count%100000 == 0:
        print(count)
   
    board = chess.Board()
    for move in black_position:
        board.push_san(move)
    
    black_bit = fen_to_bit(board.fen())
    black_bits[count,:] = black_bit
    count+=1
    #print(count)

print('saving bits')

np.save(f'bits_white_{len(white_positions)}',white_bits)
np.save(f'bits_black_{len(black_positions)}',black_bits)