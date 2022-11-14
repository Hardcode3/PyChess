# -*- coding:utf-8 -*-
__projet__ = "Chess"
__nom_fichier__ = "constants"
__author__ = "PENOT Baptiste"
__date__ = "août 2022"

from typing import Tuple


def convert_datum(cell_id_or_pos: str | Tuple[int, int]) -> Tuple[int, int] | str | None:
    """
    Convert from the tuple position to the string position depending on the input.
    :param cell_id_or_pos: the cell id (string) or the position (tuple of two integers)
    """
    if type(cell_id_or_pos) is str:
        for elt in DatumChange.DATUM_CHANGE:
            if elt[1] == cell_id_or_pos:
                return elt[0]
        raise NameError(f"The value {cell_id_or_pos} was not found in the DATUM_CHANGE list")
    elif type(cell_id_or_pos) is tuple:
        for elt in DatumChange.DATUM_CHANGE:
            if elt[0] == cell_id_or_pos:
                return elt[1]
        raise NameError(f"The value {cell_id_or_pos} was not found in the DATUM_CHANGE list")
    else:
        raise TypeError(
            f"The type {cell_id_or_pos} is not valid for this function, please enter a string or a tuple of two "
            f"integers.")


class DatumChange:
    DATUM_CHANGE: list = [
        [(0, 0), "a8"], [(0, 1), "a7"], [(0, 2), "a6"], [(0, 3), "a5"], [(0, 4), "a4"], [(0, 5), "a3"],
        [(0, 6), "a2"], [(0, 7), "a1"],
        [(1, 0), "b8"], [(1, 1), "b7"], [(1, 2), "b6"], [(1, 3), "b5"], [(1, 4), "b4"], [(1, 5), "b3"],
        [(1, 6), "b2"], [(1, 7), "b1"],
        [(2, 0), "c8"], [(2, 1), "c7"], [(2, 2), "c6"], [(2, 3), "c5"], [(2, 4), "c4"], [(2, 5), "c3"],
        [(2, 6), "c2"], [(2, 7), "c1"],
        [(3, 0), "d8"], [(3, 1), "d7"], [(3, 2), "d6"], [(3, 3), "d5"], [(3, 4), "d4"], [(3, 5), "d3"],
        [(3, 6), "d2"], [(3, 7), "d1"],
        [(4, 0), "e8"], [(4, 1), "e7"], [(4, 2), "e6"], [(4, 3), "e5"], [(4, 4), "e4"], [(4, 5), "e3"],
        [(4, 6), "e2"], [(4, 7), "e1"],
        [(5, 0), "f8"], [(5, 1), "f7"], [(5, 2), "f6"], [(5, 3), "f5"], [(5, 4), "f4"], [(5, 5), "f3"],
        [(5, 6), "f2"], [(5, 7), "f1"],
        [(6, 0), "g8"], [(6, 1), "g7"], [(6, 2), "g6"], [(6, 3), "g5"], [(6, 4), "g4"], [(6, 5), "g3"],
        [(6, 6), "g2"], [(6, 7), "g1"],
        [(7, 0), "h8"], [(7, 1), "h7"], [(7, 2), "h6"], [(7, 3), "h5"], [(7, 4), "h4"], [(7, 5), "h3"],
        [(7, 6), "h2"], [(7, 7), "h1"]]


if __name__ == '__main__':
    t = DatumChange()
    print(convert_datum("a1"))
    print(convert_datum((0, 5)))
