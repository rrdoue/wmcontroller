#! /usr/bin/env python3

from invoke import Responder
from fabric2 import Connection


def shutdown_remote_is(server):
    remote_host = server
    # Use the connection with `with` to act as a context manager
    with Connection(remote_host) as conn:
        remote_host = conn.run('hostname')
        # print(f'Connected to {remote_host})')
        # with conn.cd('/Applications/wMServiceDesigner/IntegrationServer/'):
        sudopass = Responder(
            pattern=r'Password:',
            response='\n',
        )
        result = conn.run(
            'cd /Applications/wMServiceDesigner/IntegrationServer/bin ; sudo '
            '/Applications/wMServiceDesigner/IntegrationServer/bin/shutdown.sh',
            pty=True,
            watchers=[sudopass],
        )
        summary = 'Ran {0.command!r} on {0.connection.host}, got stdout:\n{0.stdout}'
        # print(summary.format(result))
    return summary, result
