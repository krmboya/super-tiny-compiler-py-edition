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
    an associated value. e.g.

    {"type": "paren", "value": "("}

    Whitespace in the input is ignored
    """

    tokens = []

    while input_str:
        # loops while there's still unprocessed input

        # check for paren
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
    """Converts token list to abstract syntax tree

    AST node types

    program:
    {
        "type": "program",
        "body": []
    }

    number_literal:
    {
        "type": 'number_literal',
        "value": ""
    }
 
    call_expression:
    {
        "type": "call_expression",
        "name": "",
        "params": []
    }
    """

    def walk(position):
        """Parses the tokens starting from given position to AST node

        Returns the AST node and next position to resume parsing
        """

        token = tokens[position]
        if token["type"] == "number":
            # create a number_literal node type
            node = {
                "type": "number_literal",
                "value": token["value"]
            }

            # increment position and return
            position += 1
            return node, position

        if token["type"] == "paren" and token["value"] == "(":
            # Opening paren, this means we're beginning a new
            # call expression node.
            # Bulk of the parsing occurs here

            # increment position to get to the expression's name
            position += 1
            token = tokens[position]

            # begin call expression node
            call_expression_node = {
                "type": "call_expression",
                "name": token["value"],
                "params": []
            }

            # gather all the expression's params
            position += 1
            token = tokens[position]

            # peek until we see a closing paren...
            while (token["type"] != "paren" or
                   (token["type"] == "paren" and
                    token["value"] != ")")):

                # Since a param could either be a could be a nested call
                # expression or a number, we call walk() recursively
                # for each param
                param_node, position = walk(position)
                call_expression_node["params"].append(param_node)

                token = tokens[position]

            # End of call expression node. Return the node and the
            # next position resume parsing
            position += 1
            return call_expression_node, position

        # neither number nor opening paren
        msg = ("Unexpected token:" + token["type"] +
               " with value:" + token["value"])
        raise Exception(msg)

    # Root of the AST, node type 'program'
    ast = {
        "type": "program",
        "body": []
    }

    position = 0
    while position < len(tokens):
        # until we exhaust all tokens

        # get AST node starting at position
        node, position = walk(position)
        ast["body"].append(node)

    return ast


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
