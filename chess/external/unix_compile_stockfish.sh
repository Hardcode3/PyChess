#!/bin/bash

echo ""
echo "Found unix script..."
echo "Current directory", "$(pwd)"

echo "Changing directory to the Stockfish subpackage..."
cd chess/external/stockfish/src || echo "cd failed, check the structure of the project"
echo "Current directory", "$(pwd)"

STOCKFISH=stockfish

if ! test -f "$STOCKFISH"; then
  echo "$STOCKFISH executable not found, building Stockfish..."
  echo "Compiling Stockfish binaries..."
  echo "..."
  make help
  make build || echo "failed to build Stockfish, check the structure of the project"
  # todo add a way to delete temporary object files
  if test -f "$STOCKFISH"; then
    echo "$STOCKFISH executable found in $(pwd), build is a success"
  fi
else
  echo "$STOCKFISH executable found in $(pwd), binaries are already built"
fi

if ! test -f "$STOCKFISH"; then
  echo "$STOCKFISH executable not found, searching in the PATH..."
  if whereis stockfish; then
    echo "Stockfish not found in the PATH... Check its installation..."
  else
    echo "Stockfish found in PATH"
  fi
fi

# run stockfish tests
#if test -f "$STOCKFISH"; then
#  echo "launching stockfish unit tests"
#  cd ../tests || echo "test folder not found"
#  sh instrumented.sh
#  sh perft.sh
#  sh reprosearch.sh
#  sh signature.sh
#fi

# todo: add a project directory search to locate stockfih executable if it was build elsewhere

exit 0
