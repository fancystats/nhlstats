Welcome to the nhlstats library.  This library seeks to provide a robust interface for retrieving and storing game data from the NHL.

Development
===========

nhlstats is an opensource project, and we welcome pull requests.  To get started developing, we recommend you read through this document to learn how to set up a development environment and learn a bit more about the architecture of the site.

Note that most active development occurs in the dev branch.

Development Environment
-----------------------

The development environment requires Python 2.7.5 or newer and pip.  Third-party libraries can be retrieved by running `make dev-init`.  It is recommended that you make use of virtualenv and enable that prior to initializing.

Additionally you will need libffi to be installed.  On OS X you can follow the following instructions:

```
brew install pkg-config libffi
export PKG_CONFIG_PATH=/usr/local/Cellar/libffi/3.0.13/lib/pkgconfig/ # May change with libffi version
```

Note that there is also currently an issue with clang removing support for some particular C flags, so also do the following:

```
export CFLAGS=-Qunused-arguments
export CPPFLAGS=-Qunused-arguments
```

Creating a Pull Request
-----------------------

If submitting code, it is expected to pass a PEP8 linter, with the exception of line length checks.
