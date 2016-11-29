"""
Compiles Lisp style functions to C-style functions

e.g.

(add 2 3)              -> add(2, 3)
(subtract 5 1)         -> subtract(5, 1)
(add (subtract 5 1) 2) -> add( subtract(5, 1), 2)
"""

def tokenizer(input_str):
    """Returns a list of tokens

    Processes each character in the input and returns a list
    of token dicts
    
    Each token is of type `paren`, `number` or `name`, and with
    an associated value. Whitespace in the input is ignored"""

    tokens = []

    while input_str:
        # while there still unprocessed input

        # check for parens

        # check for whitespace

        # check for numbers

        # check for letters

    return tokens


