##--Dydy2412--##
from lib.labygen_unp import gen_laby_unp
from lib.labygen_exr import gen_laby_ex
from lib.labyprinter import print_to_png
from lib.labydisplay import*
import time
import sys

def gen_matrix(L_matrix, l_matrix):
    '''Generer les 3 matrices pour notre labyrynthe'''
    return [[i+((L_matrix+1)*j) for i in range(l_matrix)] for j in range(L_matrix)], [[False for i in range(l_matrix+1)] for j in range(L_matrix)], [[False for i in range(l_matrix)] for j in range(L_matrix+1)]

#---VRIABLE---#
LONG = 50
LARGE = 50

CORNER = '+'
TXTXWALL = '─'
TXTYWALL = '|'
WALL_SIZE = 10
LINE_WIDTH = 2
DESTINATION = 'laby.png'

if __name__ == '__main__':
    sys.setrecursionlimit(10000)
    
    # CELLS, VWALLS, HWALLS = gen_matrix(LONG, LARGE)
    # a = time.time()
    # CELLS, VWALLS, HWALLS = gen_laby_unp(VWALLS, HWALLS, CELLS, LONG, LARGE)
    # displayer(labydisplayer(VWALLS, HWALLS, CELLS, LONG, LARGE, CORNER, TXTXWALL, TXTYWALL, False))
    # print(time.time()-a)

    CELLS, VWALLS, HWALLS = gen_matrix(LONG, LARGE)
    a = time.time()
    CELLS, VWALLS, HWALLS = gen_laby_ex(VWALLS, HWALLS, CELLS, LONG, LARGE, True)
    displayer(labydisplayer(VWALLS, HWALLS, CELLS, LONG, LARGE, CORNER, TXTXWALL, TXTYWALL, False))
    b = time.time()
    print(b-a)

    print_to_png(VWALLS, HWALLS, LONG, LARGE, WALL_SIZE, LINE_WIDTH, DESTINATION)