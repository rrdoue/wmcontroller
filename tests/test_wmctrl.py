# import wmcontroller
import wmcontroller.wmctrl

# def test_wmctrl_not_running():
#
#     assert wmcontroller.wmctrl.component_status('rogers-mcp', 'integration server', 'status') == "Exception: HTTPConnectionPool(host='rogers-mcp', port=5555): Max retries exceeded with url: /admin/package?expand=true (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x101189ac0>: Failed to establish a new connection: [Errno 61] Connection refused'))ConnectionError on server: rogers-mcp. The integration server is not running."


def test_wmctrl_running():

    assert wmcontroller.wmctrl.component_status('rogers-mcp', 'integration server', 'status') == (200, 'The integration server is up and responding as expected.')
