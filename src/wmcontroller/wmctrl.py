#! /usr/bin/env python3

"""
Description:  Module that allows one to check status and starts, stops, or restarts
webMethods component applications.  The module can be run with direct inputs, or run
by calling other Python objects, such as a simple text-based user interface.
Inputs: Three text-based values consisting of server name, component or application,
and action.
Outputs: Results of the action, such as a status code (if available) or one-word response,
and a more descriptive statement.
"""

import argparse
from environs import env
import json
import requests
import wmrmsrvr
import sys


status_code = None  # allows the TypeError below to be caught and managed successfully with the else clause

# This reads the .env file in the current directory
env.read_env()

DEBUG = env.bool('DEBUG')
PROTOCOL = env.str('PROTOCOL')
PORT = env.str('PORT')
AUTH_USER = env.str('AUTH_USER')
AUTH_PASSWD = env.str('AUTH_PASSWD')
VERIFY_SSL_CERTIFICATE = env.bool('VERIFY_SSL_CERTIFICATE')


def component_status(server, component, action):
    headers = {
        'Accept': 'application/json',
    }

    params = {
        'expand': 'true',
    }

    if component == 'integration server':
        try:
            response = requests.get(
                f'{PROTOCOL}://{server}:{PORT}/admin/package',
                params=params,
                headers=headers,
                auth=(AUTH_USER, AUTH_PASSWD),
                timeout=10,
                verify=VERIFY_SSL_CERTIFICATE,  # note this generates a warning
            )
        except requests.ConnectionError as e:
            if DEBUG:
                print(f'\nType: {type(e)}, {e}\n')
            if 'NewConnectionError' in str(e):
                print(
                    f'\nException: {e}\nConnectionError on server: {server}. The {component} is not running.\n',
                    file=sys.stderr,
                )
            elif 'ConnectionResetError' in str(e):
                print(
                    f'\nException: {e}\nConnectionError on server: {server}. The {component} may be in the process of starting up or shutting down.\n',
                    file=sys.stderr,
                )
            exit(1)

    if DEBUG:
        try:
            print(f'{response.json()}\n')
            print(f'Server name is {server}, Status code: {response.status_code}.\n')
        except json.JSONDecodeError as e:
            print(f'\nJSON processing error: {e}\n', file=sys.stderr)

    if response.status_code == 200:  # trying multiple response options
        return (
            response.status_code,
            f'The {component} is up and responding as expected.',
        )


def component_stop(server, component, action):
    if component == 'integration server':
        fabric_summary, fabric_response = wmrmsrvr.shutdown_remote_is(server)
    return fabric_summary, fabric_response


def component_start(server, component, action):
    return f'The action `{action}` for `{component}` is not yet implemented.'


def component_restart(server, component, action):
    return f'The action `{action}` for `{component}` is not yet implemented.'


if __name__ == '__main__':
    # Create an argument parser object
    parser = argparse.ArgumentParser()

    # Define arguments for receiving inputs from the command line or other Python files
    parser.add_argument('-s', '--server', type=str, default='localhost')
    parser.add_argument('-c', '--component', type=str, default='integration server')
    parser.add_argument('-a', '--action', type=str, default='status')

    # Parse the user's arguments in sys.args according to the rules and arguments that we've defined
    command_line_args = parser.parse_args()

    if command_line_args.action == 'status':
        try:
            status_code, status_text = component_status(
                command_line_args.server,
                command_line_args.component,
                command_line_args.action,
            )
        except TypeError as e:
            print(f'\nEncountered TypeError: {e}', file=sys.stderr)

        if status_code:
            print(f'\nStatus Code: {status_code}, {status_text}\n')
            exit(0)
        else:
            # This else clause accommodates a specific login failure case used with the TypeError
            # exception above. status_code must be initially set to None for this to execute properly.
            print(
                f'Unexpected return value(s) from {command_line_args.action}, the server appears to be running, '
                f'but there is another problem (for example, a login failure).\n'
            )
            exit(1)
    elif command_line_args.action == 'stop':
        stop_summary, stop_response = component_stop(
            command_line_args.server,
            command_line_args.component,
            command_line_args.action,
        )
        print(f'Result: \n{stop_response}\n{stop_summary}\n')
    elif command_line_args.action == 'restart':
        restart_response = component_restart(
            command_line_args.server,
            command_line_args.component,
            command_line_args.action,
        )
        print(f'\n{restart_response}\n')
    elif command_line_args.action == 'start':
        start_response = component_start(
            command_line_args.server,
            command_line_args.component,
            command_line_args.action,
        )
        print(f'\n{start_response}\n')
