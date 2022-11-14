# PythonChess
A pygame wrapper for the [stockfish chess engine](https://stockfishchess.org).
For more details, check their [GitHub repository](https://github.com/official-stockfish/Stockfish).
The wrapper is based on the python package [stockfish](https://github.com/zhelyabuzhsky/stockfish.git).
The view is developped using my pygame-toolkit, helping to create gui-like views in pygame.

# Cloning
Since Stockfish is recursively cloned in the repository, clone the project as follows:
```
git clone --recursive https://github.com/Hardcode3/PythonChess.git
```
This command will also clone the Stockfish repository from GitHub so you don't have to worry about installing it.

# Launchin the app
To run the app, create a virtual environment or pip install the [requirements](requirements.txt).
## To create and activate a virtual environment on UNIX like systems
```
python3 -m venv venv
source venv/bin/activate
```
## To install the dependencies
```
pip install requirements.txt
```
After this step, pip should have installed the dependencies and you should be able to launch the main program using:
```
python3 main.py
```

# Compatibility
This version is only compatible with UNIX systems for the moment since the script for windows is not yet written.
[Stockfish for python](https://pypi.org/project/stockfish/) uses the compiled executable file available in [chess/external/src/](chess/external/src) as stockfish).

# Future improvements
- [ ] Crossplatform app
- [ ] Automatic configuration and tests of Stockfish and the a app

# Screenshots
![Main menu](assets/screenshots/main_menu.png)
![The game itself](assets/screenshots/game.png)
