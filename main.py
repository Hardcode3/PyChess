from setup import compile_stockfish
from chess.logic.game import Game

if __name__ == '__main__':
    if not compile_stockfish():
        raise FileNotFoundError("Stockfish can not be found on your system, check its installation")
    Game()
