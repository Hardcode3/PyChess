import platform
import os
import requests
import zipfile

from settings import Directories


def compile_stockfish() -> bool:
    """
    Set up the stockfish external directory by compiling the source files.
    """
    # setup for Windows
    if platform.system() == "Windows":
        print("WINDOWS platform detected")
        stockfish_win_url = (
            "https://stockfishchess.org/files/stockfish_15_win_x64_avx2.zip"
        )

        try:
            # make a request and save the content to the sockfish folder
            output_zip_file = os.path.join(
                Directories.STOCKFISH_DIR, "src/stockfish_15_win_x64_avx2.zip"
            )
            if not os.path.exists(output_zip_file):
                print(f"downloading stockfish executable from {stockfish_win_url}")
                r = requests.get(stockfish_win_url, allow_redirects=False)
                open(output_zip_file, "wb").write(r._content)
            else:
                print("existing stockfish zip file for windows found")

            executable_path: str = os.path.join(Directories.STOCKFISH_DIR, "src\stockfish_15_win_x64_avx2\stockfish_15_x64_avx2.exe")
            # extract the zipped file
            if not os.path.exists(executable_path):
                print("extracting stockfish executable...")
                with zipfile.ZipFile(output_zip_file, "r") as zipped:
                    zipped.extractall(os.path.join(Directories.STOCKFISH_DIR, "src"))
            else:
                print("existing stockfish executable for windows found")
                
            # saving the path of the stockfish executable
            Directories.STOCKFISH_EXECUTABLE = executable_path
            
            print("** stockfish is installed for windows 64 bits **")
            return True

        except:
            return False

    # setup for macOS
    elif platform.system() == "Darwin":
        print("DARWIN platform detected")
        if not os.path.exists(Directories.STOCKFISH_MAKEFILE):
            raise RuntimeError(
                "--> The Makefile script is missing, build stockfish manually in the src directory"
            )
        else:
            print(
                f"Stockfish Makefile found in {Directories.STOCKFISH_MAKEFILE}, compiling the code..."
            )
            try:
                os.system(f"sh {Directories.UNIX_CONFIG_SCRIPT}")
                if not os.path.exists(Directories.CHESS_DIR):
                    raise RuntimeError(
                        "The compilation of the stockfish engine binaries has failed, consider doing"
                        "it manually"
                    )
                else:
                    return True
            except PermissionError:
                raise PermissionError(
                    "You do not have the access rights to compile to this directory"
                )
    
    # setup for Linux
    elif platform.system() == "Linux":
        print("Linux platform detected")
        if not os.path.exists(Directories.STOCKFISH_MAKEFILE):
            raise RuntimeError(
                "--> The Makefile script is missing, build stockfish manually in the src directory"
            )
        else:
            print(
                f"Stockfish Makefile found in {Directories.STOCKFISH_MAKEFILE}, compiling the code..."
            )
            try:
                os.system(f"sh {Directories.UNIX_CONFIG_SCRIPT}")
                if not os.path.exists(Directories.CHESS_DIR):
                    raise RuntimeError(
                        "The compilation of the stockfish engine binaries has failed, consider doing"
                        "it manually"
                    )
                else:
                    return True
            except PermissionError:
                raise PermissionError(
                    "You do not have the access rights to compile to this directory"
                )

    else:
        raise OSError("Invalid operating system")


if __name__ == "__main__":
    compile_stockfish()
