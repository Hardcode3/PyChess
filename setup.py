import platform
import os
from settings import Directories


def compile_stockfish() -> bool:
    """
    Set up the stockfish external directory by compiling the source files.
    """
    # setup for Windows
    if platform.system() == "Windows":
        # todo set up the project for windows
        pass

    # setup for macOS
    elif platform.system() == "Darwin":
        if not os.path.exists(Directories.STOCKFISH_MAKEFILE):
            raise RuntimeError("--> The Makefile script is missing, build stockfish manually in the src directory")
        else:
            print(f"Stockfish Makefile found in {Directories.STOCKFISH_MAKEFILE}, compiling the code...")
            try:
                os.system(f"sh {Directories.UNIX_CONFIG_SCRIPT}")
                if not os.path.exists(Directories.CHESS_DIR):
                    raise RuntimeError("The compilation of the stockfish engine binaries has failed, consider doing"
                                       "it manually")
                else:
                    return True
            except PermissionError:
                raise PermissionError("You do not have the access rights to compile to this directory")
    else:
        raise OSError("Invalid operating system")


if __name__ == '__main__':
    compile_stockfish()
