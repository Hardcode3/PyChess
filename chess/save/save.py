import os
from settings import (
    Directories,
    Settings
)
from contextlib import contextmanager


class Save:
    """
    Class handling one save of the game
    To store multiple saves, use multiple instances of the Save class
    """

    def __init__(self, path: str, absolute_path: bool = False) -> None:
        self.path_: str = path
        if absolute_path:
            if not os.path.exists(self.path_):
                print(f"absolute path @ {self.path_}")
                print(f"The absolute path for the save of the game does not exists :"
                      f"{self.path_}, creating a new save file")
                self.create_save()
        elif not absolute_path:
            self.path_ = os.path.join(Directories.SAVE_DIR, self.path_)
            print(f"The relative path for the save of the game does not exists"
                  f"{self.path_}, creating a new save file in {self.path_}")
            if not os.path.exists(os.path.join(Directories.SAVE_DIR, self.path_)):
                self.create_save()
            print(f"relative path @ {self.path_}")
        else:
            pass

    def create_save(self) -> None:
        with open(self.path_, "w") as fs:
            fs.write(Settings.FEN_POSITION_BEGIN)

    def write_save(self, fen: str) -> None:
        """
        @brief Writes the save file as a fen string for the considered index
        @param fen the fen notation corresponding to the game state
            (this fen can then be loaded by the chess engine to resume the game)
        """
        print(f"writing save @ {self.path_}")
        with open(self.path_, "w") as sf:
            sf.write(fen)

    def load_save(self) -> str:
        """
        @brief Loads the save by reading the save file
        """
        with open(self.path_, "r") as sf:
            return sf.readline()

    @staticmethod
    def is_saved(saved_fen: str, current_fen: str) -> bool:
        """
        Check if the last save is the current state of the game.
        If both states are the same, then returns True, otherwise return False.
        """
        if current_fen == current_fen:
            return True
        return False


@contextmanager
def filestream(path: str, mode: str) -> None:
    """
    @brief a filestream to write data in a file
    @path the path of the file to create, override or read
    @mode the mode, read or write (resp. "r", "w")

    use this function with:

        with filestream("file.txt", "w") as file:
            file.write("blabla")

    """
    f = open(path, mode)
    yield f
    f.close()


if __name__ == '__main__':
    save_1 = Save("save_1.txt", absolute_path=False)
    save_2 = Save("save_2.txt", absolute_path=False)
    save_3 = Save("save_3.txt", absolute_path=False)
    save_4 = Save("save_4.txt", absolute_path=False)
    save_5 = Save("save_5.txt", absolute_path=False)
