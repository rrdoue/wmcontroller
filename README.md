Running some of Reuven's suggestions to set up a project with uv

### Prerequisite: Ensure that uv is installed, this was new for me and I used the following recommendation:

# Note the following:
Reference:  https://docs.astral.sh/uv/getting-started/installation/#standalone-installer
#
"PyPI

"For convenience, uv is published to PyPI.

"If installing from PyPI, we recommend installing uv into an isolated environment, for example, with pipx:"

$ pipx install uv
#
Rogers-MacBook-Pro:~ rrdoue$ pipx install uv
  installed package uv 0.6.13, installed using Python 3.12.5
  These apps are now globally available
    - uv
    - uvx
done! ✨ 🌟 ✨
Rogers-MacBook-Pro:~ rrdoue$ which uv
/Users/rrdoue/.local/bin/uv
### End Prerequisite

In the planned project directory `wmcontroller`,

Rogers-MacBook-Pro:wmcontroller rrdoue$ pwd
/Users/rrdoue/Documents/code/python/projects/wmcontroller

Rogers-MacBook-Pro:wmcontroller rrdoue$ uv init
Initialized project `wmcontroller`

Rogers-MacBook-Pro:wmcontroller rrdoue$ ls -l
total 16
-rw-r--r--@ 1 rrdoue  staff    0 Apr 17 17:31 README.md
-rw-r--r--@ 1 rrdoue  staff   90 Apr 17 17:31 main.py
-rw-r--r--@ 1 rrdoue  staff  158 Apr 17 17:31 pyproject.toml

Rogers-MacBook-Pro:wmcontroller rrdoue$ uv venv
Using CPython 3.12.5 interpreter at: /Library/Frameworks/Python.framework/Versions/3.12/bin/python3.12
Creating virtual environment at: .venv
Activate with: source .venv/bin/activate

Rogers-MacBook-Pro:wmcontroller rrdoue$ ls -al
total 32
drwxr-xr-x@  9 rrdoue  staff  288 Apr 17 17:32 .
drwxr-xr-x@ 10 rrdoue  staff  320 Apr  7 11:03 ..
drwxr-xr-x@  9 rrdoue  staff  288 Apr  7 11:04 .git
-rw-r--r--@  1 rrdoue  staff  661 Dec 22 20:34 .gitignore
-rw-r--r--@  1 rrdoue  staff    5 Apr 17 17:31 .python-version
drwxr-xr-x@  7 rrdoue  staff  224 Apr 17 17:32 .venv
-rw-r--r--@  1 rrdoue  staff    0 Apr 17 17:31 README.md
-rw-r--r--@  1 rrdoue  staff   90 Apr 17 17:31 main.py
-rw-r--r--@  1 rrdoue  staff  158 Apr 17 17:31 pyproject.toml

# In adding required packages for the project, I had a problem where I'd manually added the environs and requests packages to the pyproject.toml file prior to using uv to install them.  I temporarily removed environs and requests, whereupon uv cleaned up the manually edited pyproject.toml file, removing the manual entries for those packages.  Then I reran the installations to see that uv updates the project file as expected.

Rogers-MacBook-Pro:wmcontroller rrdoue$ uv remove requests
Resolved 4 packages in 330ms
Uninstalled 5 packages in 17ms
 - certifi==2025.1.31
 - charset-normalizer==3.4.1
 - idna==3.10
 - requests==2.32.3
 - urllib3==2.4.0
Rogers-MacBook-Pro:wmcontroller rrdoue$ uv remove environs
Resolved 1 package in 1ms
Uninstalled 3 packages in 5ms
 - environs==14.1.1
 - marshmallow==4.0.0
 - python-dotenv==1.1.0

# Now reinstall those packages

Rogers-MacBook-Pro:wmcontroller rrdoue$ uv add environs
Resolved 4 packages in 2ms
Installed 3 packages in 4ms
 + environs==14.1.1
 + marshmallow==4.0.0
 + python-dotenv==1.1.0
Rogers-MacBook-Pro:wmcontroller rrdoue$ uv add requests
Resolved 9 packages in 281ms
Installed 5 packages in 6ms
 + certifi==2025.1.31
 + charset-normalizer==3.4.1
 + idna==3.10
 + requests==2.32.3
 + urllib3==2.4.0

# Now the pyproject.toml file contains the updated packages with versioning information as follows:

[project]
name = "wmcontroller"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
requires-python = ">=3.12"
dependencies = [
    "environs>=14.1.1",
    "requests>=2.32.3",
]

# Now add pytest, with the --dev modifier

Rogers-MacBook-Pro:wmcontroller rrdoue$ uv add --dev pytest
Resolved 14 packages in 1.93s
Prepared 4 packages in 477ms
Installed 4 packages in 7ms
 + iniconfig==2.1.0
 + packaging==24.2
 + pluggy==1.5.0
 + pytest==8.3.5

# and pyproject.toml reflects the installation:

... 
[dependency-groups]
dev = [
    "pytest>=8.3.5",
]


# Reuven built the package at this point ...

uv build

# which added a file in dist

# check the build file with tar tzvf <build_file> as desired

# extract the build in /tmp using tar -zxvf <build_file> as desired

# Now write some tests in the tests directory and run the tests with pytest.  Note I just tried Reuven's sample to see how it works for me, and it does.

But install the new module first:

Rogers-MacBook-Pro:wmcontroller rrdoue$ pwd
/Users/rrdoue/Documents/code/python/projects/wmcontroller

Rogers-MacBook-Pro:wmcontroller rrdoue$ uv pip install . # install to current directory
Resolved 9 packages in 704ms
      Built wmcontroller @ file:///Users/rrdoue/Documents/code/python/projects/wmcon
Prepared 1 package in 1.33s
Installed 1 package in 1ms
 + wmcontroller==0.1.0 (from file:///Users/rrdoue/Documents/code/python/projects/wmcontroller)

# Add to the pytest test_myprog.py file:
from wmcontroller.myprog import hello

Rogers-MacBook-Pro:wmcontroller rrdoue$ uv run pytest

# and those tests ran successfully:

Rogers-MacBook-Pro:wmcontroller rrdoue$ uv run pytest tests/test_myprog.py -v
=============================== test session starts ================================
platform darwin -- Python 3.12.5, pytest-8.3.5, pluggy-1.5.0 -- /Users/rrdoue/Documents/code/python/projects/wmcontroller/.venv/bin/python3
cachedir: .pytest_cache
rootdir: /Users/rrdoue/Documents/code/python/projects/wmcontroller
configfile: pyproject.toml
collected 3 items

tests/test_myprog.py::test_hello[world-Hello, world!] PASSED                 [ 33%]
tests/test_myprog.py::test_hello[-Hello, !] PASSED                           [ 66%]
tests/test_myprog.py::test_hello[5-Hello, 5!] PASSED                         [100%]

================================ 3 passed in 0.00s =================================

# Although my project tests are failing, the purpose of this was just to confirm that we can use uv to create a project following the layout with a working pytest configuration.
