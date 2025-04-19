#! /usr/bin/env python3

"""
Reference Reuven's rrdoue_pydab6-yet_more-python-functions.ipynb (rrdoue colab document) class Exercise 3a,
the menu module get_choice function.  In this sub-exercise, we go through the process of setting up the
background process for organizing the choices into something that can be used for presenting to the user a
list of choices.
"""


def menu(*args):  # accept any number of arguments
    Debug = None

    output = {}  # return a key-value selection
    key_lookup = {}

    if Debug:
        print(f'Index and Values')

    for idx, argument in enumerate(args, start=1):
        key_lookup[str(idx)] = argument
        if Debug:
            print(f'{idx}: {argument}')

    if Debug:
        print(f'\n')
        print(f'{key_lookup}')

    while True:
        # print(f'Choices:')
        for key, value in key_lookup.items():
            print(f'{key}  {value}')  # ({key}):

        user_response: str = input(
            f'\nPlease enter the number of your choice: '
        ).strip()

        if user_response in key_lookup.keys():
            return key_lookup[user_response]
