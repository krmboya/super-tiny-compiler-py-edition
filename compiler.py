#!/usr/bin/env python
"""
Compiles Lisp style functions to C-style functions

e.g.

(add 2 3)              -> add(2, 3)
(subtract 5 1)         -> subtract(5, 1)
(add (subtract 5 1) 2) -> add( subtract(5, 1), 2)
"""
import re

def tokenizer(input_str):
    """Returns a list of tokens from source string

    Process each character in the input and return a list
    of tokens representing the relevant ones.
    
    Each token is of type `paren`, `number` or `name`, and with
    an associated value. Whitespace in the input is ignored"""

    tokens = []

    while input_str:
        # loops while there's still unprocessed input

        # check for parens
        if input_str[0] in ('(', ')',):
            tokens.append(
                dict(type="paren", value=input_str[0])
            )
            input_str = input_str[1:]  # remove the processed section loop
            continue                   

        # check for whitespace
        whitespace_match = re.match(r'\s+', input_str)
        if whitespace_match:
            match_length = len(whitespace_match.group())
            input_str = input_str[match_length:]
            continue

        # check for numbers
        number_match = re.match(r'\d+', input_str)
        if number_match:
            numbers = number_match.group()
            tokens.append(
                dict(type="number", value=numbers)
            )
            input_str = input_str[len(numbers):]
            continue

        # check for letters
        letter_match = re.match(r'[a-zA-Z]+', input_str)
        if letter_match:
            letters = letter_match.group()
            tokens.append(
                dict(type="name", value=letters)
            )
            input_str = input_str[len(letters):]
            continue

        raise Exception("Unknown token")

    return tokens


def parser(tokens):
    return tokens


def transformer(ast):
    return ast


def code_generator(new_ast):
    return new_ast


def compiler(src):
    output = code_generator(transformer(parser(tokenizer(src))))
    return output


if __name__ == "__main__":
    src = "(add (subtract 5 1) 2)"
    output = compiler(src)
    print output
