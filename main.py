import webbrowser as wb
import json
import sys
import requests as rq
import itertools
def to_pgn_symbol(str):
    bishop = ['\\v','\\b']
    knight = ['\\m','\\n']
    queen = ['\\q','\\w']
    rook = ['\\t','\\r']
    king = ['\\l','\\k']
    str = str.replace(bishop[0], 'B')
    str = str.replace(bishop[1], 'B')
    str = str.replace(knight[0], 'N')
    str = str.replace(knight[1], 'N')
    str = str.replace(queen[0], 'Q')
    str = str.replace(queen[1], 'Q')
    str = str.replace(rook[0], 'R')
    str = str.replace(rook[1], 'R')
    str = str.replace(king[0], 'K')
    str = str.replace(king[1], 'K')
    return str

if len(sys.argv) > 1:
    game_url = sys.argv[1]
else:
    game_url = input("Enter the game's url: ")

id = game_url[game_url.find('game')+5:game_url.rfind('/')]
req_url = f'https://www.drawbackchess.com/app7/game?id={id}'

with rq.get(req_url) as resp:
    if not resp.ok:
        print('Could not send request. Exiting...')
        exit()
    moves = resp.json()['game']['scoreSheet']
    pgn = ''
    for k,v in list(moves.items())[:-1]:
        if '–' in v[0]:
            break
        pgn += to_pgn_symbol(v[0]) + '_'
        if len(v) == 2:
            if '–' in v[1]:
                break
            pgn += to_pgn_symbol(v[1]) + '_'
    pgn = pgn.replace('\\0', '').replace('OOO', 'O-O-O')\
            .replace('OO', 'O-O')
    wb.open(f'https://lichess.org/analysis/pgn/{pgn}')