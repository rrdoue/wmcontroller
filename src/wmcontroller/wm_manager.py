#! /usr/bin/env python3

"""
Description:  Wrapper or workflow process that accepts user input and calls the wmctrl
module to check status or start, stop, and restart webMethods component applications.
This can be run with direct inputs, or run interactively with simple menus that ask
the user for input based on a pre-configured set of menus based on the webMethods
environment, on one to many servers.
Inputs: Two forms, three text-based values consisting of server name, component or
application, action.  If run without all inputs, the application prompts the user for
input using menus that must be configured in the accompanying menu.py file prior to use.
Outputs: Results of the action, such as a status code (if available), and descriptive
text.
"""

import argparse
import menu
import wmctrl
import wmrmsrvr

Debug = None  # None or True

# Create an argument parser object for checking user input
parser = argparse.ArgumentParser()

# Define the arguments to allow for flexibility
parser.add_argument('-s', '--server', nargs='?', const='')
parser.add_argument('-c', '--component', nargs='?', const='')
parser.add_argument('-a', '--action', nargs='?', const='')

# Parse the user's arguments in sys.args according to the rules and arguments that we've defined
args = parser.parse_args()

if Debug:
    print(f'DEBUG:args is {args}, Namespace type is type({args.__dict__})')

if args.server is None or args.component is None or args.action is None:
    print(
        f'This script manages webMethods components, typically running on one server or as '
        f'part of a weMethods cluster.  The following questions guide you through the '
        f'process of requesting an action for one of the component applications.\n'
    )

    print(f'Please select the server:')
    server = menu.menu('rogers-imac', 'rogers-mcp')
    if Debug:
        print(f'DEBUG:Server is {server}')

    print(f'Please select the component (or application):')
    component = menu.menu(
        'integration server',
        'broker',
        'universal messaging',
        'terracotta cluster',
        'My WebMethods Server',
        'Command Central',
    )
    if Debug:
        print(f'DEBUG:Component is {component}')

    print(f'Please select the action:')
    action = menu.menu('status', 'start', 'stop', 'restart')
    if Debug:
        print(f'DEBUG:Action is {action}')

    print(f'\nYou are requesting {action} for {component} on {server}.\n')
    confirm = input(f'Is this correct (y or n)?: ')
else:
    print(
        f'\nYou are requesting {args.action} for the {args.component} on {args.server}.\n'
    )
    confirm = input(
        f'Please confirm the {args.action} for the {args.component} on {args.server} (y or n): '
    )
    if confirm == 'y' or confirm == 'yes':
        print(f'\nYou responded y (yes), proceeding ... ')
        if args.component == 'integration server' and args.action == 'status':
            status_code, status_text = wmctrl.component_status(
                args.server, args.component, args.action
            )
            print(f'\nStatus code: {status_code}. {status_text}\n')
            exit(0)
        elif args.component == 'integration server' and args.action == 'stop':
            stop_summary, stop_response = wmrmsrvr.shutdown_remote_is(args.server)
            print(f'Result: \n{stop_response}\n{stop_summary}\n')
            exit(0)
    elif confirm == 'n' or reconfirm == 'no':
        print(f'\nYou responded n (no), exiting.\n')
        exit(0)

if confirm == 'y' or confirm == 'yes':
    print(f'You responded y (yes).\n')
    reconfirm = input('Proceed? y or n: ')
    if reconfirm == 'y' or reconfirm == 'yes':
        if component == 'integration server' and action == 'status':
            status_code, status_text = wmctrl.component_status(server, component, action)
            print(f'\nStatus code: {status_code}. {status_text}\n')
            exit(0)
        elif component == 'integration server' and action == 'stop':
            if Debug:
                print('In the stop action if statement.\n')
            stop_summary, stop_response = wmrmsrvr.shutdown_remote_is(server)
            print(f'Result: \n{stop_response}\n{stop_summary}\n')
            exit(0)
    elif reconfirm == 'n' or reconfirm == 'no':
        print(f'\nYou responded n (no), exiting.\n')
        exit(0)
elif confirm == 'n' or confirm == 'no':
    print(f'\nYou responded n (no), exiting.\n')
    exit(0)
