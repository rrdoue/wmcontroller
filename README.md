Description:  Module that allows one to check status and starts, stops, or restarts webMethods component applications remotely.  The module can be run with direct inputs, or run by calling other Python objects, such as through a simple text-based user interface.

Limitations: The functionality is limited to checking webMethods Integration Server status and stopping or shutting down the Integration Server component.

Setup and Configuration:

1. Using a text editor, set the user and password manually in the wmctrl.py file component_status() function, line 41.

2. For the simple text-based user interface provided by the wm_manager.py file, update the list of host or server names on line 44.

Inputs: Typically three text-based values consisting of server name, component or application, and action.

For example, ./wmctrl.py -s 'host_name' -c 'integration server' -a 'status', where the script connects using an https connection.

In addition, there is a simple text-based manager, wm_manager.py, that guides the user through selecting a server, component, and action, then performs the action after comfirmation from the user.  Please remember to update the file as recommended in Setup and Configuration (above), updating the server or host names for your environment.

Outputs: Results of the action, such as a http status code (if available) or one-word response, and a more descriptive statement for the status.  The stop action simply returns the standard response one sees when running the vendor's shutdown script.