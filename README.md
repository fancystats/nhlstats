About FancyStats
================

The FancyStats project aims to provide a high quality, flexible source of traditional and advanced NHL statistics to the intarwebs.  Born out of a frustration with a lack of easil digestible NHL stats, the project hopes to remove the repeated effort of individuals having to screen scrape existing sources.

The project also seeks to allow advanced users the felxibility to explore the data directly, with the ability to create custom stats and answer questions more easily.

If you are just looking to make use of the stats, you should head over to [fancystats.org](fancystats.org) and start exploring today!  If you are a developer looking to contribute to the site or learn more about how it works, you can find more information on the code that drives the site below.

Development
===========

FancyStats is an opensource project, and we welcome pull requests.  To get started developing, we recommend you read through this document to learn how to set up a development environment and learn a bit more about the architecture of the site.

Site Architecture
-----------------

FancyStats is broken up into three major parts:

* cron tasks, which handle gathering data from the NHL and adding it to our database at regular intervals.
* an API, which is used by the site's front-end as well as users looking to get access to the raw data.
* front-end, which presents data to casual visitors of the site.

These pieces are discrete, and may eventually be broken up into separate repositories, but for now live together in this repo.

In addition to these pieces, a database is required to store the results.  For our production instance, we run PostgreSQL, but our use of SQLALchemy should allow the use of any supported SQL database.

###Cron Tasks

Our cron tasks consist of the screen scraping tools that run regularly on the server, collecting data from the NHL.  The tasks check our database on start up for active games, and will check the games for updates to data, entering any new information in the database.  Additionally, we run less frequent checks for corrections to past games.

The test suite for this code includes static assets we've downloaded from the NHL, to represent various issues we need to test for in the code (missing information, incorrect information, etc.)

The code is written in Python and makes use of Scrapy for web scraping and SQLAlchemy for interacting with the database.

###API

The API layer exists to present the data in the database to clients on the web.  It is written in Python and makes use of Flask-API to provide a simple web API.

The test suite for this code focuses on encoding issues and dealing with bad data.

###Front-End

The front end is a static AngularJS site, which is intended to be hosted on a service such as S3 for maximum uptime.  The site connects to the API 

The test suite for this code focuses on dealing with poor connections, bad data, and encoding issues.

Development Environment
-----------------------

The development environment requires Python 2.7.5 or newer and pip.  Third-party libraries can be retrieved by running `make dev-init` inside each of the project components subdirectories.  It is recommended that you make use of virtualenv and enable that prior to initializing.

Additionally you will require libffi to be installed.  On OS X you can follow the following instructions:

```
brew install pkg-config libffi
export PKG_CONFIG_PATH=/usr/local/Cellar/libffi/3.0.13/lib/pkgconfig/ # May change with libffi version
```

Note that there is also currently an issue with clang removing support for some particular C flags, so also do the following:

```
export CFLAGS=-Qunused-arguments
export CPPFLAGS=-Qunused-arguments
```

If submitting code, it is expected to pass a PEP8 linter, with the exception of line length checks.

